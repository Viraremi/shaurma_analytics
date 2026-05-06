# Описание конфигурационного файла (.env)
<table>
  <thead>
    <tr>
      <th>Переменная</th>
      <th>Описание</th>
    </tr>
  </thead>
  <tbody>
    <!-- Категория 1 -->
    <tr>
      <td colspan="2" align="center"><strong>🤖 Telegram Bot & Admin</strong></td>
    </tr>
    <tr>
      <td><code>BOT_TOKEN</code></td>
      <td>Уникальный токен бота от @BotFather</td>
    </tr>
    <tr>
      <td><code>ADMIN_ID</code></td>
      <td>Числовой ID администратора для доступа к спец. функциям</td>
    </tr>
    <tr>
      <td><code>ADMIN_WORD</code></td>
      <td>Секретная фраза/пароль для верификации действий</td>
    </tr>
    <!-- Категория 2 -->
    <tr>
      <td colspan="2" align="center"><strong>💬 Группы и Топики</strong></td>
    </tr>
    <tr>
      <td><code>TEST_GROUP</code></td>
      <td>ID группы, предназначенной для тестирования</td>
    </tr>
    <tr>
      <td><code>TEST_TOPIC</code></td>
      <td>ID темы (Thread ID) внутри тестовой группы</td>
    </tr>
    <tr>
      <td><code>DEPARTAMENT_GROUP</code></td>
      <td>ID официальной группы департамента</td>
    </tr>
    <tr>
      <td><code>DEPARTAMENT_TOPIC</code></td>
      <td>ID темы (Thread ID) внутри группы департамента</td>
    </tr>
    <!-- Категория 3 -->
    <tr>
      <td colspan="2" align="center"><strong>🗄 База данных</strong></td>
    </tr>
    <tr>
      <td><code>DB_HOST</code></td>
      <td>Адрес сервера БД (например, 127.0.0.1 или db_container)</td>
    </tr>
    <tr>
      <td><code>DB_PORT</code></td>
      <td>Порт подключения (по умолчанию 5432)</td>
    </tr>
    <tr>
      <td><code>DB_NAME</code></td>
      <td>Имя используемой базы данных</td>
    </tr>
    <tr>
      <td><code>DB_USER</code></td>
      <td>Имя пользователя для авторизации</td>
    </tr>
    <tr>
      <td><code>DB_PASS</code></td>
      <td>Пароль для доступа к БД</td>
    </tr>
  </tbody>
</table>