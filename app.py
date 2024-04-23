import atexit
import base64
import time
from datetime import datetime
from traceback import format_exc

import firebase_admin
import httpx
import uvicorn
from fastapi import FastAPI, Request, responses
from fastapi.exceptions import HTTPException
from firebase_admin import credentials, db

app = FastAPI()


client = httpx.AsyncClient()
atexit.register(client.aclose)
START = datetime.now()
cred = credentials.Certificate(
{
  "type": "service_account",
  "project_id": "teleking-62908",
  "private_key_id": "e512e0945ad4241a69d962d6002777e640164cbb",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQChjetu7+Osuw4Q\nJH2QJT96NJ3Rmz0wUEDBrrQke4dOcRr303/lu/5Dq0FOBAn6DczIuk4ysm/KxmbE\nwPMNSWqQ+qgo8qp49lq4sGSphpmFo5v+4cm2HLZeWq++wTD/ZusytBIit+5SvpGc\nb8oqjsM5IwudmPU9JpmJnnoq6oNttfcm9A9gebHMVxVZacQBos6AsH+BrUYe/tHy\njcfsk8HJXJviEJznu3wPh4h0BjOJx4expbJZnacG5VzzIvwXLbnRff6NW0dDL9sp\nmoyGn1FD2Bvnn1L6BH/q41j8tDHRosKM+61Q42IKyV/kvv7g3CtPxVxHR9OjxoDY\nZ8hzo75/AgMBAAECggEAAITWrUALAKqHJIkheB2OgyN5IEu52hZf5t9bR8S3zgox\n9nrQ7dl5OxlpN8luiMWTk0954dLN5h5WBSrDfRbvxzBu6tbAsmvEJdS3Ng4vHw1D\n+oEaJ0IXWd07tEallCRt+/c1GbRyiQSArjpzsUhNGzlgF6z+mKgvlRATv2CKdIdA\nSXgvovE2qXgpDEmrIpzBNa0iDXDD2uFJn8O4n6UJ1C+OHXj/Nmu4buXTvTbp8JKl\nH+xlXe8iu9lAU6Ea6TMQ3YG812PcFwzmFWH0vKJLcu8vMh0t6gy572V8Ebpf50ef\nP9aWeGY2HnXjF/zYDLZSp7L6KOPfwGNcNqZ0Yx9DcQKBgQDXf6RVJIlR5Y3bknPH\nSRamyOcYmlGMnCvbCLtF2b3yTnPAFzzXZ0avoSlKucPiX6k325fDjcz4hCgJTQAd\nTi8PqMs/HUQ6S/Pcp6mnss9spM2TgX12jaxXZtmsXRMWeJbBvlNnb/YsrACzCHv0\nK2bKP5N+oLvII2LZHR5NZLKl0QKBgQC/6tczFdAFE2RDkcuD+vYtRkSQKdxHBCu9\nFS8SWch3CVcpl5zRw20SN1MhGO7Ss3DFHJDskgt1+ox3q7EccD5vFlSuQaG3Vhua\ncN3l7yMZPs2RKEKprKElU31AIJwVFE2j0eVQO08WJjm2IkQ2bAlNk/yG22iasEqZ\nu7DO4ScjTwKBgBGKC//6B0spGdCjLNUtd7B/bX+tH7IIC/G51jQrMrCD/hvGSGdn\nunMU9N1mHTFRg95N+x4pbmNTrkaDg9zevinSHSi34xOzlteAteg2P3eiOjElOubp\nRPugHVtP//u2ON7v9K3YiPq9zRjFOgF3ftg7MG//+QijCKqPGiZGadvhAoGAWT+P\nth0FsOaUsOuDFixGAUX1Komc+5WP9Y19Z25DUEASva/Y6J+WAGukB/c9UNTLs46W\nQr2kAMh0PE6mvY/hKO3ckXDKEKVFjuu/9WbhDqNrG376iUdTZTVPQNwpWZAoju9U\nUZxTKfy6x91llV1mciJIxDoSiiVDe/yRu5NvDPcCgYBFKzdeH0/ew1nEhIf2pgVB\nhlP1EqYxJT6Woo129/p7UUrS5mKMH3JBMRYBq+2fiEoIo4KFrhRmBVQ/oVmR0qtF\nIx4H7XiXs1e5IG36554OKT6vzAncXcAD2iA9qM0lgGzhvNJfz7crd0Ha/S//Msrl\nZA1Atg639KU3X6ObjFWcig==\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-1k8lo@teleking-62908.iam.gserviceaccount.com",
  "client_id": "110226883990471118748",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-1k8lo%40teleking-62908.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}

)

firebase_admin.initialize_app(
    cred, {"databaseURL": "https://teleking-62908-default-rtdb.firebaseio.com/"}
)

updb = db.reference("trxpayUpdates")
botdb = db.reference("trxpay").get() or {}

USED = []
PROXY = {}
SAFE_IP = []
DUPLICATE = {}


def create_dup():
    for z in list(botdb):
        try:
            user = int(z)
            data = botdb[z]
            ip = data["ip"]
            DUPLICATE[ip] = user
        except BaseException:
            pass


create_dup()


async def send_message(msg: dict):
    print(msg)
    if not isinstance(msg, dict):
        return
    updb.push(msg)


@app.get("/when")
async def wn():
    try:
        return {"start": str(START), "now": str(datetime.now())}
    except BaseException:
        return str(format_exc())


@app.get("/verify", response_class=responses.HTMLResponse)
async def vf(id: str = ""):
    if not id:
        return responses.HTMLResponse(
            content="<h1>Invalid Request</h1>", status_code=404
        )
    chtml = open("./web/verify.html", "r").read()
    chtml = chtml.replace("{{ id }}", id)
    return responses.HTMLResponse(content=chtml, status_code=200)


@app.get("/tq", response_class=responses.HTMLResponse)
async def vfd(request: Request, id: str, device: str):
    data = eval(base64.b64decode(id))
    county, ip = "", ""
    for x, y in request.headers.raw:
        if b"x-vercel-ip-country" == x or b"cf-ipcountry" in x:
            county = y.decode("utf-8")
        elif b"client-ip" in x or b"real-ip" in x:
            ip = y.decode("utf-8")
    if ip and DUPLICATE.get(ip) and DUPLICATE[ip] != data["user"]:
        chtml = open("./web/f4.html", "r").read()
        return responses.HTMLResponse(content=chtml, status_code=200)
    if ip and ip not in SAFE_IP:
        try:
            if ip in list(PROXY):
                if data["user"] not in PROXY[ip]:
                    PROXY[ip].append(data["user"])
                    await send_message({"proxy": ip, "user": data["user"]})
                chtml = open("./web/f3.html", "r").read()
                return responses.HTMLResponse(content=chtml, status_code=200)
            js = (await client.get(f"https://v2.api.iphub.info/guest/ip/{ip}")).json()
            if (js.get("block") or 0) == 1:
                PROXY[ip] = [data["user"]]
                await send_message({"proxy": ip, "user": data["user"]})
                chtml = open("./web/f3.html", "r").read()
                return responses.HTMLResponse(content=chtml, status_code=200)
            SAFE_IP.append(ip)
            DUPLICATE[ip] = data["user"]
            if not js.get("block"):
                print(js)
        except BaseException:
            pass
    data.update({"country": county, "ip": ip, "device": device})
    await send_message(data)
    chtml = open("./web/tq.html", "r").read()
    return responses.HTMLResponse(content=chtml, status_code=200)


@app.get("/mystery", response_class=responses.HTMLResponse)
async def claim(id: str = ""):
    try:
        if not id:
            raise HTTPException(400, "Missing ID")
        data = eval(base64.b64decode(id))
        if id in USED or (data["time"] < time.time()):
            chtml = open("./web/f2.html", "r").read()
        else:
            chtml = open("./web/captcha.html", "r").read()
            chtml = chtml.replace("{{ id }}", id)
        return responses.HTMLResponse(content=chtml, status_code=200)
    except BaseException:
        return responses.HTMLResponse(
            content=f"<h1>Invalid Request</h1><p>{format_exc()}", status_code=404
        )


@app.get("/claim", response_class=responses.HTMLResponse)
async def claimed(id: str, request: Request):
    try:
        if not id:
            raise HTTPException(400, "Missing ID")
        data = eval(base64.b64decode(id))
        if id in USED or (data["time"] < time.time()):
            chtml = open("./web/f2.html", "r").read()
        else:
            USED.append(id)
            ip = ""
            for x, y in request.headers.raw:
                if b"x-vercel-ip-country" == x or b"cf-ipcountry" in x:
                    data["country"] = y.decode("utf-8")
                elif b"client-ip" in x or b"real-ip" in x:
                    data["ip"] = ip = y.decode("utf-8")
            if ip and DUPLICATE.get(ip) and DUPLICATE[ip] != data["user"]:
                chtml = open("./web/f4.html", "r").read()
                return responses.HTMLResponse(content=chtml, status_code=200)
            if ip and ip not in SAFE_IP:
                try:
                    if ip in list(PROXY):
                        if data["user"] not in PROXY[ip]:
                            PROXY[ip].append(data["user"])
                            await send_message({"proxy": ip, "user": data["user"]})
                        chtml = open("./web/f3.html", "r").read()
                        return responses.HTMLResponse(content=chtml, status_code=200)
                    js = (
                        await client.get(f"https://v2.api.iphub.info/guest/ip/{ip}")
                    ).json()
                    if (js.get("block") or 0) == 1:
                        PROXY[ip] = [data["user"]]
                        await send_message({"proxy": ip, "user": data["user"]})
                        chtml = open("./web/f3.html", "r").read()
                        return responses.HTMLResponse(content=chtml, status_code=200)
                    SAFE_IP.append(ip)
                    if not js.get("block"):
                        print(js)
                    DUPLICATE[ip] = data["user"]
                except BaseException:
                    pass
            await send_message(data)
            chtml = open("./web/s2.html", "r").read()
        return responses.HTMLResponse(content=chtml, status_code=200)
    except BaseException:
        return responses.HTMLResponse(
            content=f"<h1>Invalid Request</h1><p>{format_exc()}", status_code=404
        )


########################################################


@app.get("/", response_class=responses.HTMLResponse)
async def main():
    # chtml = open("./web/main.html", "r").read()
    return responses.HTMLResponse(
        content="<h1>You Are Not Supposed To Be Here</h1>", status_code=200
    )


if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=80,
        reload=True,
        proxy_headers=True,
        forwarded_allow_ips="*",
    )
