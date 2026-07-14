# E-WALLET
## Video Demo:
https://youtu.be/V2EvmR7RXTE
## Introduction:
As the final project of CS50x, I have made a website as my project namely E-Wallet. Objective of E-wallet.xxx is to use for managing income vis a vis monthly expenses while making some saving.
## Programming Languages:
- I've used Python, HTML, CSS, Javascript and SQL.
- I've used flask web framework based in Python using Python, HTML, CSS, Javascript and SQL.
## Website`s features are explained below
### It has five pages namely login, home, income, monthly expenses, summary
## 1. Log-in
### **• Register:**
User`s have to register to use this website.
```html
{% extends "layout.html" %}

{% block title %}
    Register
{% endblock %}
{% block main %}
    <div class="register">
        <body class="login1">
    <form action="/register" method="post">
        <label class="bg-danger" for="username">
            <i class="fas fa-user-alt"></i>
        </label>
            <input autocomplete="off" autofocus id="username" name="username" placeholder="Username" type="text" required>

            <label class="bg-danger" for="password">
                <i class="fas fa-lock"></i>
            </label>
            <input id="password" name="password" placeholder="Password" type="password" required>
            <label class="bg-danger" for="password">
                <i class="fas fa-lock"></i>
            </label>
            <input id="confirmation" name="confirmation" placeholder="Password(again)" type="password" required>
            <p class="msg">{{ msg }}</p>
            <input class="bg-danger" type="submit" value="Register">
    </form>
</body>
      </div>
{% endblock %}
```
<img src="Screenshot (1).png">

### **• If username is already taken to register:**

if users type the same username as someone else’s username during the registration process, it'll tell them that the username has already been taken so they’ll have to type another username.

```sql
all_users = db.execute("SELECT username FROM users;")
```
```python
        for i in range(len(all_users)):
            if username == all_users[i]["username"]:
                return render_template("register.html", msg="Sorry, username has taken!")
```
<img src="Screenshot (2).png">

### **• Password don’t match in register:**
if users type a wrong password in the confirm password field, it'll tell that the password didn’t match.

```python
username = request.form.get("username")
 password = request.form.get("password")
 confirmation = request.form.get("confirmation")
 if request.method == "POST":
    if not confirmation in password:
       return render_template("register.html", msg="The password don't match")
```
<img src="Screenshot (3).png">

### **•	Login:**
Users will have to login using the already registered user name.
```html
{% block title %}
    Log In
{% endblock %}

{% block main %}
    <div class="login">
        <body class="login1">
    <form action="/login" method="post">
            <label class="bg-danger" for="username">
                <i class="fas fa-user-alt"></i>
            </label>
            <input autocomplete="off" autofocus id="username" name="username" placeholder="Username" type="text" required>
            <label class="bg-danger" for="password">
                <i class="fas fa-lock"></i>
            </label>
            <input id="password" name="password" placeholder="Password" type="password" required>
        <p class="msg">{{ msg }}</p>
        <input class="bg-danger" type="submit" value="Login">
    </form>
</body>
</div>
{% endblock %}
```
<img src="Screenshot (4).png">

### **•	Login invalid username/password:**
If users type the wrong username/password by mistake, it'll tell username/password invalid.
```sql
rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
```
```python
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return render_template("login.html", msg="invalid username/password")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
```
<img src="Screenshot (5).png">

## 2. Homepage:
- Home page shows that the title is E-wallet and will tell us that you can manage your budget and expenses by using E-wallet.
- You can see on which page you are via the highlight on the navigation bar. To make this feature, I have used Javascript and CSS.
```html
{% extends "layout.html" %}

{% block title %}
    Home
{% endblock %}

{% block main %}
       <form action="/" method="post">
                <body class="home">
                <h1 class="home1">E-Wallet</h1>
                <p class="home2">You can manage your Budget and Expences by using E-Wallet</p>
            </body>
       </form>
{% endblock %}
```
```javascript
 <script src="http://code.jquery.com/jquery-2.1.4.min.js">
    </script>
    <script>
        $(function(){
            $('a').each(function(){
                if ($(this).prop('href') == window.location.href) {
                    $(this).addClass('active'); $(this).parents('li').addClass('active');
                }
            });
        });
    </script>
```
```css
#navbar .active {
    color: #ffffff;
}
```
<img src="Screenshot (6).png">

## 3. Income:
When you input income for each day/month, you must suppose your income is in dollars. As you can see, when you enter any amount in income field, its saved with date so it'll help you revisit later.
### **• When you input any amount in the income, this will add income showing in front of cash.**
```
     income = int(request.form.get("income"))
     cash1 = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
     cash2 = cash1[0]['cash']
     cash2 += income
     db.execute("UPDATE users SET cash = ? WHERE id = ?", cash2, session["user_id"])
```
### **• Users also have the option to start with monthly expenses.**
first you click on the tab “monthly expenses” and you fill in the expenses. Then you click on the tab “income” and you type in the income. Then you’ll be able to see how much cash is left.
```
cash0 = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
        s = db.execute("SELECT spend2 FROM sum WHERE user_id = ?", session["user_id"])
        if cash0[0]['cash'] == 0:
           cash0[0]['cash'] = 0
        else:
            spends = db.execute("SELECT spend2 FROM sum WHERE user_id = ?", session["user_id"])
            total_s2 = 0
            for i in spends:
                total_s2 += i['spend2']
            cash12 = cash0[0]['cash'] - total_s2
            db.execute("UPDATE users SET cash = ? WHERE id = ?", cash12, session["user_id"])
```
<img src="Screenshot (7).png">

## 4. Monthly Expenses:
We have to fill in the expected expenses e.g. home rent, groceries, utilities etc. This will now calculate how much expenses we have each month and how much we are left with. It will calculate and tell us our monthly expense.
### **• When users fill in the expenses e.g. homerent, groceries, utilities etc, these will be recorded in the monthly table in SQL**
```
def monthly():
    if request.method == "POST":
        now = datetime.now()
           datetime1 = now.strftime("%Y/%m/%d %H:%M:%S")
        db.execute("INSERT INTO monthly (id, homerent, groceries, eb, shopping, other, datetime, travel, petrol, loan, education, weekly) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", session["user_id"], request.form.get("homerent"), request.form.get("groceries"), request.form.get("eb"), request.form.get("shopping"), request.form.get("other"), datetime1, request.form.get("travel"), request.form.get("petrol"), request.form.get("loan"), request.form.get("education"), request.form.get("weekly"))
```
### **•	I have made a loop to calculate the total expenses each day. This will record in sum table in SQL**
```
add = db.execute("SELECT spend2, homerent, groceries, eb, shopping, other, travel, petrol, loan, education, weekly FROM monthly WHERE id = ?", session["user_id"])
        total = 0
        for i in add:
            i['spend2'] += i['homerent']
            i['spend2'] += i['groceries']
            i['spend2'] += i['eb']
            i['spend2'] += i['shopping']
            i['spend2'] += i['other']
            i['spend2'] += i['travel']
            i['spend2'] += i['petrol']
            i['spend2'] += i['loan']
            i['spend2'] += i['education']
            i['spend2'] += i['weekly']
        total += i['spend2']
        db.execute("INSERT INTO sum (spend2, user_id) VALUES (?, ?)",       i['spend2'], session["user_id"])
```
### **•	I made a loop to calculate how much is left in cash, if we have recorded any expenses.**
```
cash0 = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
        if cash0[0]['cash'] == 0:
           cash0[0]['cash'] = 0
        else:
            s = db.execute("SELECT spend2 FROM sum WHERE user_id = ?", session["user_id"])
            for i in (s):
                cash12 = cash0[0]['cash'] - i['spend2']
            db.execute("UPDATE users SET cash = ? WHERE id = ?", cash12, session["user_id"])
```
<img src="Screenshot (8).png">

## 5. Summary:
This is a great way to calculate everything without keeping any notepads and diaries and we can note down all our expenses in one place.
I have used SQL, python, CSS and HTML.
```
def summary():
    spends = db.execute("SELECT spend2 FROM sum WHERE user_id = ?", session["user_id"])
    total_s = 0
    for i in spends:
        total_s += i['spend2']
    db.execute("UPDATE users SET spend1 = ? WHERE id = ?", total_s, session['user_id'])
    total_s1 = db.execute("SELECT spend1 FROM users WHERE id = ?", session["user_id"])
    cash10 = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
    monthly1 = db.execute("SELECT * FROM monthly WHERE id = ?", session["user_id"])
    return render_template("list.html", total_s1=total_s1, cash10=cash10, monthly1=monthly1)
{% extends "layout.html" %}

{% block title %}
    Summary
{% endblock %}

{% block main %}
<body class="summary2">
    <form action="/summary" method="post">
        <table>
            <thead>
                <thead>
                    <div class="mb-4">
                  <h1 style="color:white;font-size:40px;text-align:center;">SUMMARY</h1>
                    </div>
                </thead>
                <tr>
                    <th style="color:white;" class="text-startr">Date</th>
                    <th style="color:white;" class="text-start">Home Rent</th>
                    <th style="color:white;" class="text-start">Groceries</th>
                    <th style="color:white;" class="text-start">Utilities:(Electricity Bill+Gas Bill)</th>
                    <th style="color:white;" class="text-start">Shopping</th>
                    <th style="color:white;" class="text-start">Travel</th>
                    <th style="color:white;" class="text-start">Petrol/Diesel</th>
                    <th style="color:white;" class="text-start">Loan payment</th>
                    <th style="color:white;" class="text-start">Education</th>
                    <th style="color:white;" class="text-start">Weekly Outing</th>
                    <th style="color:white;" class="text-start">Other</th>
                    <div class="vertical"></div>
                    <th style="color:white;" class="text-start">Total Spend</th>
                </tr>
            </thead>
            <tbody>
                {% for i in monthly1 %}
                <tr>
                    <td style='font-weight:bold;color:white;' class="text-center">{{ i.datetime }}</td>
                    <td style='font-weight:bold;color:white;' class="text-start">{{ i.homerent | usd }}</td>
                    <td style='font-weight:bold;color:white;' class="text-start">{{ i.groceries | usd }}</td>
                    <td style='font-weight:bold;color:white;' class="text-start">{{ i.eb | usd }}</td>
                    <td style='font-weight:bold;color:white;' class="text-start">{{ i.shopping | usd }}</td>
                    <td style='font-weight:bold;color:white;' class="text-start">{{ i.travel | usd }}</td>
                    <td style='font-weight:bold;color:white;' class="text-start">{{ i.petrol | usd }}</td>
                    <td style='font-weight:bold;color:white;' class="text-start">{{ i.loan | usd }}</td>
                    <td style='font-weight:bold;color:white;' class="text-start">{{ i.education | usd }}</td>
                    <td style='font-weight:bold;color:white;' class="text-start">{{ i.weekly | usd }}</td>
                    <td style='font-weight:bold;color:white;' class="text-start">{{ i.other | usd }}</td>
                    <td style='font-weight:bold;color:white;' class="text-start">{{ i.spend2 | usd }}</td>
                </tr>
                {% endfor %}
                <tr>
                <!-- TODO: Loop through the database entries to display them in this table -->
                    <td style="color:white;" class="border-0 fw-bold text-end" colspan="11">Expenses</td>
                    <td style='font-weight:bold;color:white;' class="text-end">{{ total_s1[0]["spend1"] | usd }}</td>
                  </tr>
                <tr>
                  <!-- TODO: Loop through the database entries to display them in this table -->
                  <td style="color:white;" class="border-0 fw-bold text-end" colspan="11">Cash</td>
                  <td style='font-weight:bold;color:white;' class="text-end">{{ cash10[0]['cash'] | usd }}</td>
                </tr>
            </tbody>
        </table>
    </form>
</body>
{% endblock %}
```
<img src="Screenshot (9).png">
<img src="Screenshot (10).png">

## **Databases:**
I made four tables in SQL.
- First table: This has user’s table. It has id, username, hash, cash and spend1. Spend1 means that how much overall total expenses have been made. Notice that id must be primary key.
- Second table: This has a monthly expense’s table. It has id, datetime, monthly_id, home rent, groceries, utilities etc. Id means user’s id. Monthly_id must be primary key.
- Third table: This has a sum’s table. It has id, user_id and spend2. Spend2 means that how much total expenses have been made each day. Id is primary key.
- Fourth table:  This has an income’s table. It has id, user_id, income1 and datetime1. When user inputs income in the field “income”, it will be recorded in the table in dollars. Notice that id is primary key.

## **About CS50:**
CS50 is a course from Havard University and taught by David J. Malan. This course about the computer science and programming languages. This course teaches students how to think algorithmically and solve problems efficiently. Topics include abstraction, algorithms, data structures, encapsulation, resource management, security, and software engineering. Languages include C, Python, and SQL plus students’ choice of: HTML, CSS, and JavaScript (for web development).

Thank you for all CS50.


