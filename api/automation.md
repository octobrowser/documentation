# Automation Libraries

Drive Octo Browser profiles from Selenium, Playwright, Puppeteer, and similar Chromium-automation frameworks. The pattern is the same in every language:

1. Use the **cloud API** (`https://app.octobrowser.net/api/v2/automation`) to manage profiles.
2. Use the **local client API** (`http://127.0.0.1:58888`) to start a profile with `debug_port: true`.
3. Connect your automation library to the returned `ws_endpoint` (CDP WebSocket) or `debug_port`.

## Prerequisites

- Octo Browser desktop app running and signed in.
- A profile UUID (from the dashboard or `GET /profiles`).
- The automation library of your choice installed in your environment.

See [profiles.md](profiles.md) for profile creation and [local-client.md](local-client.md) for the start/stop API.

## Puppeteer (Node.js)

Connects via `browserWSEndpoint` from the local start response.

```javascript
const puppeteer = require('puppeteer');
const axios = require('axios');

const OCTO_REMOTE_API = axios.create({
  baseURL: 'https://app.octobrowser.net/api/v2/automation/',
  timeout: 2000,
  headers: { 'X-Octo-Api-Token': 'YOUR_API_TOKEN' },
});

const OCTO_LOCAL_API = axios.create({
  baseURL: 'http://127.0.0.1:58888/api/profiles/',
  timeout: 100000,
});

async function createProfile() {
  const { data } = await OCTO_REMOTE_API.post('/profiles', {
    title: 'API Test profile',
    fingerprint: { os: 'win' },
  });
  return data;
}

async function startProfile(uuid) {
  const { data } = await OCTO_LOCAL_API.post('/start', {
    uuid,
    headless: true,
    debug_port: true,
  });
  return data;
}

(async () => {
  const created = await createProfile();
  const started = await startProfile(created.data.uuid);
  const browser = await puppeteer.connect({
    browserWSEndpoint: started.ws_endpoint,
    defaultViewport: null,
  });
  const page = await browser.newPage();
  await page.goto('https://google.com/');
})();
```

## Pyppeteer (Python)

```python
import asyncio
import logging
import os

import httpx
import pyppeteer

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(name)s: %(message)s')
log = logging.getLogger('octo')

OCTO_TOKEN = os.getenv('OCTO_TOKEN', 'PUT_TOKEN_HERE')
OCTO_API = 'https://app.octobrowser.net/api/v2/automation/profiles'
LOCAL_API = 'http://localhost:58888/api/profiles/start'
HEADERS = {'X-Octo-Api-Token': OCTO_TOKEN}


async def get_profile(cli):
    profiles = (await cli.get(OCTO_API, headers=HEADERS)).json()
    return profiles['data'][0]['uuid']


async def get_cdp(cli):
    uuid = await get_profile(cli)
    resp = (await cli.post(LOCAL_API, json={'uuid': uuid, 'debug_port': True})).json()
    return resp['ws_endpoint']


async def main():
    async with httpx.AsyncClient() as cli:
        ws_url = await get_cdp(cli)
    browser = await pyppeteer.launcher.connect(browserWSEndpoint=ws_url)
    try:
        page = await browser.newPage()
        await page.goto('https://duckduckgo.com/')
    finally:
        await browser.close()


if __name__ == '__main__':
    asyncio.run(main())
```

## Playwright (Node.js)

```javascript
const axios = require('axios');
const pw = require('playwright');

const OCTO_REMOTE_API = axios.create({
  baseURL: 'https://app.octobrowser.net/api/v2/automation/',
  timeout: 2000,
  headers: { 'X-Octo-Api-Token': 'YOUR_API_TOKEN' },
});

const OCTO_LOCAL_API = axios.create({
  baseURL: 'http://127.0.0.1:58888/api/profiles/',
  timeout: 100000,
});

async function createProfile() {
  const { data } = await OCTO_REMOTE_API.post('/profiles', {
    title: 'API Test profile',
    fingerprint: { os: 'win' },
  });
  return data;
}

async function startProfile(uuid) {
  const { data } = await OCTO_LOCAL_API.post('/start', {
    uuid,
    headless: false,
    debug_port: true,
  });
  return data;
}

(async () => {
  const created = await createProfile();
  const started = await startProfile(created.data.uuid);
  const browser = await pw.chromium.connectOverCDP(started.ws_endpoint);
  const context = browser.contexts()[0];
  const page = context.pages()[0];
  await page.goto('https://google.com');
})();
```

## Playwright Sync Python

```python
import httpx
from playwright.sync_api import sync_playwright

PROFILE_UUID = "UUID_OF_YOUR_PROFILE"


def main():
    with sync_playwright() as p:
        start_response = httpx.post(
            'http://127.0.0.1:58888/api/profiles/start',
            json={'uuid': PROFILE_UUID, 'headless': False, 'debug_port': True},
        )
        if not start_response.is_success:
            print(f'Start response is not success: {start_response.json()}')
            return
        ws_endpoint = start_response.json().get('ws_endpoint')
        browser = p.chromium.connect_over_cdp(ws_endpoint)
        page = browser.contexts[0].pages[0]
        page.goto('https://google.com')
        browser.close()


if __name__ == '__main__':
    main()
```

## Playwright Async Python

```python
import asyncio
import httpx
from playwright.async_api import async_playwright

PROFILE_UUID = "UUID_OF_YOUR_PROFILE"


async def main():
    async with async_playwright() as p:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                'http://127.0.0.1:58888/api/profiles/start',
                json={'uuid': PROFILE_UUID, 'headless': False, 'debug_port': True},
            )
            if not response.is_success:
                print(f'Start response is not successful: {response.json()}')
                return
            ws_endpoint = response.json().get('ws_endpoint')
        browser = await p.chromium.connect_over_cdp(ws_endpoint)
        page = browser.contexts[0].pages[0]
        await page.goto('https://google.com')
        await browser.close()


if __name__ == '__main__':
    asyncio.run(main())
```

## Selenium (Python)

> **Heads-up:** Selenium is detectable by some anti-bot solutions. If you hit detection issues, switch to Puppeteer/Playwright or [undetected-chromedriver](https://github.com/ultrafunkamsterdam/undetected-chromedriver).

```python
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

PROFILE_ID = 'PROFILE_UUID'
WEBDRIVER_PATH = Service(executable_path=r'./chromedriver/chromedriver-win64/chromedriver.exe')
LOCAL_API = 'http://localhost:58888/api/profiles'


def get_webdriver(port):
    chrome_options = Options()
    chrome_options.add_experimental_option('debuggerAddress', f'127.0.0.1:{port}')
    return webdriver.Chrome(service=WEBDRIVER_PATH, options=chrome_options)


def get_debug_port(profile_id):
    data = requests.post(
        f'{LOCAL_API}/start',
        json={'uuid': profile_id, 'headless': False, 'debug_port': True},
    ).json()
    return data['debug_port']


def main():
    port = get_debug_port(PROFILE_ID)
    driver = get_webdriver(port)
    driver.get('http://amazon.com')


if __name__ == '__main__':
    main()
```

## Selenium (Java)

```java
import org.apache.http.client.methods.CloseableHttpResponse;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClients;
import org.apache.http.util.EntityUtils;
import org.json.JSONObject;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;

public class Main {
    private static final String PROFILE_ID = "PROFILE_UUID";
    private static final String CHROME_DRIVER = "./path/to/chromedriver.exe";
    private static final String LOCAL_API = "http://127.0.0.1:58888/api/profiles";

    public static void main(String[] args) throws Exception {
        int port = getDebugPort(PROFILE_ID);
        WebDriver driver = getWebDriver(port);
        driver.get("http://google.com");
    }

    public static WebDriver getWebDriver(int port) {
        ChromeOptions chromeOptions = new ChromeOptions();
        chromeOptions.setExperimentalOption("debuggerAddress", "127.0.0.1:" + port);
        System.setProperty("webdriver.chrome.driver", CHROME_DRIVER);
        return new ChromeDriver(chromeOptions);
    }

    public static int getDebugPort(String profileId) throws Exception {
        try (CloseableHttpClient httpClient = HttpClients.createDefault()) {
            HttpPost httpPost = new HttpPost(LOCAL_API + "/start");
            JSONObject json = new JSONObject();
            json.put("uuid", profileId);
            json.put("headless", false);
            json.put("debug_port", true);
            httpPost.setEntity(new StringEntity(json.toString()));
            httpPost.setHeader("Accept", "application/json");
            httpPost.setHeader("Content-type", "application/json");
            try (CloseableHttpResponse response = httpClient.execute(httpPost)) {
                JSONObject responseJson = new JSONObject(EntityUtils.toString(response.getEntity()));
                return responseJson.getInt("debug_port");
            }
        }
    }
}
```

## Selenium (Visual Basic .NET)

```vbnet
Imports System
Imports System.Net.Http
Imports System.Text
Imports Newtonsoft.Json.Linq
Imports OpenQA.Selenium
Imports OpenQA.Selenium.Chrome

Module Program
    Public Class Main
        Private Shared ReadOnly PROFILE_ID As String = "PROFILE_UUID_SHOULD_BE_HERE"
        Private Shared ReadOnly CHROME_DRIVER As String = "./chromedriver-win64/chromedriver.exe"
        Private Shared ReadOnly LOCAL_API As String = "http://127.0.0.1:58888/api/profiles"

        Public Shared Sub Main(args As String())
            Dim port As Integer = GetDebugPort(PROFILE_ID)
            Dim driver As IWebDriver = GetWebDriver(port)
            driver.Navigate().GoToUrl("http://google.com")
        End Sub

        Public Shared Function GetWebDriver(port As Integer) As IWebDriver
            Dim chromeOptions As New ChromeOptions()
            chromeOptions.DebuggerAddress = "127.0.0.1:" & port
            Environment.SetEnvironmentVariable("webdriver.chrome.driver", CHROME_DRIVER)
            Return New ChromeDriver(chromeOptions)
        End Function

        Public Shared Function GetDebugPort(profileId As String) As Integer
            Dim debugPort As Integer
            Using httpClient As New HttpClient()
                Dim httpPost As New HttpRequestMessage(HttpMethod.Post, LOCAL_API & "/start")
                Dim json As New JObject()
                json("uuid") = profileId
                json("headless") = False
                json("debug_port") = True
                httpPost.Content = New StringContent(json.ToString(), Encoding.UTF8, "application/json")
                httpPost.Headers.Accept.ParseAdd("application/json")
                Using response = httpClient.SendAsync(httpPost).Result
                    Dim responseJson As JObject = JObject.Parse(response.Content.ReadAsStringAsync().Result)
                    debugPort = responseJson("debug_port")
                End Using
            End Using
            Return debugPort
        End Function
    End Class
End Module
```

## Best Practices

1. **Stop profiles** when automation finishes (`POST /api/profiles/stop`) — abandoned profiles block re-launch.
2. **Use `ws_endpoint`** when the framework supports it (Puppeteer, Playwright) — `debug_port` is convenient for Selenium's `debuggerAddress` only.
3. **Pin `debug_port`** when running many profiles in parallel to avoid port-allocation races (`debug_port: 20000` and so on, valid range `1024–65534`).
4. **Use chromedrivers** matching your installed Chromium build — get them from [chrome-for-testing](https://googlechromelabs.github.io/chrome-for-testing/).

## Common Issues

- **Connection refused** — Octo Browser app not running, or the profile was started without `debug_port: true`.
- **Profile already running** — call `GET /api/profiles/active`, then `POST /api/profiles/stop` (or `force_stop`) before re-launching.
- **Detected by anti-bot** — switch from Selenium to Puppeteer/Playwright, or use undetected-chromedriver.
- **Timeouts on slow proxies** — raise the start `timeout` (in seconds) in the `POST /api/profiles/start` body.
