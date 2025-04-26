# Auth

### Authorixation with OAuth

- В общих чертах про oauth и какие есть grant types: <https://auth0.com/intro-to-iam/what-is-oauth-2>
- Oauth2 Authorization code flow (with urls, but just concept without code): <https://auth0.com/docs/get-started/authentication-and-authorization-flow/authorization-code-flow/call-your-api-using-the-authorization-code-flow>
- Зачем нужен "authorization-code" в OAuth 2.0 (почему бы не отправлять токен авторизации при первом запросе на авторизационный сервер): <https://stackoverflow.com/questions/15219006/oauth2-0-why-need-authorization-code-and-only-then-the-token>
- Полная реализация использования oauth2 на реакте (с картинками по тому, как получать токены в админке гугла и бэком на node.js): <https://tasoskakour.com/blog/react-use-oauth2>
- Реализация OAuth2 чисто на фронте с использованием хука: <https://tasoskakour.com/blog/react-use-oauth2>
- rfc oauth2: <https://datatracker.ietf.org/doc/html/rfc6749#section-4.4>
- Хорошо про oauth2 на русском, но без примеров с кодом: <https://skillbox.ru/media/code/chto-takoe-oauth-20-ponyatie-i-printsip-raboty/>


### Usage of JWT token

- Разница между авторизацией и аутентификацией: <https://habr.com/ru/companies/banki/articles/862516/>
- Про сессионные токены, возможные способы реализации session management: <https://supertokens.com/blog/all-you-need-to-know-about-user-session-security>
- Интересный способ реализации session management: <https://supertokens.com/blog/the-best-way-to-securely-manage-user-sessions>
- Сравнение использования JWT токена и opaque токена: <https://supertokens.com/blog/are-you-using-jwts-for-user-sessions-in-the-correct-way>
- (устарел, но ок) Статья про реализацию oauth2 в django + react (часть 1): <https://www.hacksoft.io/blog/google-oauth2-with-django-react-part-1>
- (устарел, но ок) Статья про реализацию oauth2 в django + react (часть 2): <https://www.hacksoft.io/blog/google-oauth2-with-django-react-part-2>
- (свежая) Статья про реализацию oauth2 в django + react: <https://www.hacksoft.io/blog/adding-google-login-to-your-existing-django-and-django-rest-framework-applications>
- Реализация на django Google OAuth and flake8: https://github.com/HackSoftware/Django-React-GoogleOauth2-Example/tree/main/server
- Реализация на django Google Login Server Flow: https://github.com/HackSoftware/Django-Styleguide-Example/tree/master/styleguide_example/blog_examples/google_login_server_flow
- Что хранить в Blacklist: https://stackoverflow.com/questions/38897514/what-to-store-in-a-jwt
- Django styleguide (есть немного про тесты и моки): https://github.com/HackSoftware/Django-Styleguide/?tab=readme-ov-file

User sessions involve managing tokens across your app’s backend and frontend. These tokens act as a proxy to your’s identity and can either be:

Opaque (a.k.a session tokens – a long random meaningless string which is a reference to some information stored in a database)
Non-opaque (contains some meaningful information like a userID, encoded in base64)
Non opaque tokens have a special property that enables the backend to verify that the token is legitimate. This is achieved by cryptographically signing them, and in doing so, we get what is known as a JWT – a signed, non-opaque token.

Myth: No need to ask users for ‘cookie consent’: Cookie consent which is required for GDPR, applies only to cookies used for analytics and tracking. Not for keeping users logged in securly. JWTs and opaque tokens are the same in regards to this point.

Cookies

- В бородатые годы не было localStorage и sessionStorage, поэтому данные на клиенте можно было хранить только в куках
- Есть ограничение на около 100 кук на домен и размер не более 4kb
- хедер Set-Cookie: yummy_cookie=chocolate (может быть несколько в запросе)
- Опции для выставления кук: https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Cookies#security
- js-cookie: https://dev.to/codeparrot/react-cookies-a-complete-guide-to-managing-cookies-in-react-applications-3cd3


### My instruction for google OAuth

- Go to <https://support.google.com/googleapi/answer/6158849?hl=en>. Choose `clients`.
- Set:
  - Authorized JavaScript origins: `http://localhost:3000` and `http://localhost:8000`
  - Authorized redirect URIs: `http://localhost:8000/auth/oauth/google/callback` (server side) or `http://localhost:3000/auth/callback` (client side)
- Wait

