from API import Security

username =  "123"
useragent = "Mozilla/5.0"

s = Security()
token = s.generate_token(username, useragent)
print(token, flush=True)