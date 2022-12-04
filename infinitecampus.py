import json
import urllib.parse
import requests
import httpx
import base64
import sys


def ic_token(base64token: str) -> dict:
  "Converts the Base64 cookie information to a dict"
  
  jsontext = base64.urlsafe_b64decode(base64token)
  return json.loads(jsontext.decode())


def get_crits_and_grades(token: str, id: str) -> str:
  "Get criterions and their grades by class ID, returns JSON"

  # The result of everything.
  result = {
    "criterions": None,
    "grades": None
  }

  cookies: dict = ic_token(token)

  # Get the criterions (and PBIS scores, too!)
  # It's up to the JavaScript client to process all this shit.
  headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    # 'Cookie': 'JSESSIONID=C1AD32C3EF93FD4E52ADF280BAE3F336; _did-566357552=8c907765-05ee-43e5-9a7a-09a8b3ec400f; XSRF-TOKEN=4f0ce87b-853b-4a10-a4fd-1989f881ab14; tool=; selection=; portalApp=student; portalLang=en; sis-cookie=!F1MJBSI38kdaeNUUQ+LwrCQnI3Hsxbh+QFUkPb5alD3jDIPrH0NvTwqVo0Ert/EQZsd6TwC3U3MzUOo=; appName=milwaukee',
    'Expires': '0',
    'Referer': f"https://milwaukeewi.infinitecampus.org/campus/apps/portal/student/classroom/tabs/{id}/grades",
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Chromium";v="107", "Not=A?Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
}

  response = requests.get(
      f"https://milwaukeewi.infinitecampus.org/campus/resources/portal/grades/detail/{id}",
      cookies=cookies,
      headers=headers,
  )

  result["criterions"] = response.text

  # Get the grades
  headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    # 'Cookie': 'JSESSIONID=C1AD32C3EF93FD4E52ADF280BAE3F336; _did-566357552=8c907765-05ee-43e5-9a7a-09a8b3ec400f; XSRF-TOKEN=4f0ce87b-853b-4a10-a4fd-1989f881ab14; tool=; selection=; portalApp=student; portalLang=en; sis-cookie=!F1MJBSI38kdaeNUUQ+LwrCQnI3Hsxbh+QFUkPb5alD3jDIPrH0NvTwqVo0Ert/EQZsd6TwC3U3MzUOo=; appName=milwaukee',
    'Expires': '0',
    'Referer': f"https://milwaukeewi.infinitecampus.org/campus/apps/portal/student/classroom/tabs/{id}/grades",
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Chromium";v="107", "Not=A?Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
}

  response = requests.get(
      f"https://milwaukeewi.infinitecampus.org/campus/api/portal/assignment/byDateRange?startDate=2020-12-03T00:00:00&endDate=2099-12-17T00:00:00&sectionID={id}",
      cookies=cookies,
      headers=headers,
  )

  result["grades"] = response.text
  return json.dumps(result)
  

  

def get_classes(token: str) -> str:
  "Get classes based off of Infinite Campus token, returns JSON."
  
  cookies: dict = ic_token(token)

  headers = {
      'Accept': 'application/json, text/plain, */*',
      'Accept-Language': 'en-US,en;q=0.9',
      'Cache-Control': 'no-cache',
      'Connection': 'keep-alive',
      # Requests sorts cookies= alphabetically
      # 'Cookie': '_did-566357552=4876da50-00dd-401b-8f58-c49415c044ee; tool=; selection=; portalApp=student; JSESSIONID=C9048B2F21476CE3A046EA41A1DCE3AB; XSRF-TOKEN=3ed6b0c7-a064-417e-8bc1-3388f7faaa35; portalLang=en; sis-cookie=!gXvm/92HbyALEPkUQ+LwrCQnI3HsxTuYoMdFBpYBVrdpZU9uY3Qxyy639BAiV2p6gIuH8Vcw/5RQDMQ=; appName=milwaukee',
      'Expires': '0',
      'Referer': 'https://milwaukeewi.infinitecampus.org/campus/apps/portal/student/grades',
      'Sec-Fetch-Dest': 'empty',
      'Sec-Fetch-Mode': 'cors',
      'Sec-Fetch-Site': 'same-origin',
      'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
      'sec-ch-ua': '"Chromium";v="107", "Not=A?Brand";v="24"',
      'sec-ch-ua-mobile': '?0',
      'sec-ch-ua-platform': '"Linux"',
  }

  response = requests.get('https://milwaukeewi.infinitecampus.org/campus/resources/portal/grades', cookies=cookies, headers=headers)

  return response.text
  

def login(username, password) -> str:  
  "Logs in with a username and password, returns Base64 cookie information."
  
  url = "https://milwaukeewi.infinitecampus.org/campus/verify.jsp"

  password_url = urllib.parse.quote(password)  
  
  payload = f"username={username}&password={password_url}&portalUrl=portal%2Fstudents%2Fmilwaukee.jsp%3F%26rID%3D0.778348687641898&appName=milwaukee&url=nav-wrapper&lang=en&portalLoginPage=students"
  
  headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    # 'Cookie': ''
  }
  
  response = httpx.post(url, headers=headers, data=payload)
  json_text = json.dumps(dict(response.cookies))
  return base64.urlsafe_b64encode(json_text.encode()).decode()


def get_multiple_grades(token, assignment_id) -> str:
  cookies: dict = ic_token(token)
  
  headers = {
      'Accept': 'application/json, text/plain, */*',
      'Accept-Language': 'en-US,en;q=0.9',
      'Cache-Control': 'no-cache',
      'Connection': 'keep-alive',
      # 'Cookie': '_did-566357552=8c907765-05ee-43e5-9a7a-09a8b3ec400f; tool=; selection=; portalApp=student; JSESSIONID=F84D9BA4ECBC96E4C67B477576326E6E; XSRF-TOKEN=4e8ac4c6-5baa-439a-be91-5257489efa3b; portalLang=en; sis-cookie=!F1MJBSI38kdaeNUUQ+LwrCQnI3Hsxbh+QFUkPb5alD3jDIPrH0NvTwqVo0Ert/EQZsd6TwC3U3MzUOo=; appName=milwaukee',
      'Expires': '0',
      'Referer': 'https://milwaukeewi.infinitecampus.org/campus/apps/portal/student/classroom/tabs/2661529/curriculum/resource/2356751/view?classroomSectionID=2661529',
      'Sec-Fetch-Dest': 'empty',
      'Sec-Fetch-Mode': 'cors',
      'Sec-Fetch-Site': 'same-origin',
      'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
      'sec-ch-ua': '"Chromium";v="107", "Not=A?Brand";v="24"',
      'sec-ch-ua-mobile': '?0',
      'sec-ch-ua-platform': '"Linux"',
  }

  params = {
  #  'personID': '344558',
  }
  
  response = requests.get(
      f"https://milwaukeewi.infinitecampus.org/campus/api/instruction/curriculum/sectionContent/{assignment_id}",
      params=params,
      cookies=cookies,
      headers=headers,
  )
  
  return response.text
