# Authentication System Implementation Plan

## Status: MODELS UPDATED ✅

The database models have been successfully updated with User authentication. Here's what needs to happen next:

## ⚠️ BREAKING CHANGES

The new authentication system completely changes the database schema. You will need to:

1. **Delete the old database**: `rm -f study_groups.db`
2. **Run the new seed script** (after updating it)
3. **All existing data will be lost**

## Files Already Updated

### ✅ models.py
- Added `User` model with Flask-Login UserMixin
- Updated `StudyGroup`: `host_name` → `host_id` (Foreign Key)
- Updated `Participant`: `name` → `user_id` (Foreign Key)
- Updated `DiscussionPost`: `author_name` → `author_id` (Foreign Key)
- Updated `DiscussionReply`: `author_name` → `author_id` (Foreign Key)
- Added password hashing methods
- Added user activity methods

### ✅ requirements.txt
- Added Flask-Login==0.6.3
- Added Flask-Bcrypt==1.0.1
- Added email-validator==2.1.0

## Next Steps (In Order)

### Step 1: Update forms.py ⏳
Remove name fields from existing forms and add new auth forms:

```python
# REMOVE from CreateStudyGroupForm:
- host_name field

# REMOVE from JoinStudyGroupForm:
- name field (entire form can be simplified to just CSRF)

# REMOVE from CreateDiscussionPostForm:
- author_name field

# REMOVE from CreateDiscussionReplyForm:
- author_name field

# ADD new forms:
class RegistrationForm(FlaskForm):
    email = StringField (with @princeton.edu validation)
    username = StringField (unique, 3-20 chars)
    full_name = StringField
    password = PasswordField (min 8 chars)
    confirm_password = PasswordField (must match)
    class_year = SelectField (2026, 2027, 2028, 2029)

class LoginForm(FlaskForm):
    email_or_username = StringField
    password = PasswordField
    remember_me = BooleanField (optional)

class EditProfileForm(FlaskForm):
    full_name = StringField
    class_year = SelectField
    new_password = PasswordField (optional)
    confirm_password = PasswordField
```

### Step 2: Update app.py 🔄
Major changes needed:

```python
# ADD imports:
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import User, bcrypt
from forms import RegistrationForm, LoginForm, EditProfileForm

# Initialize Flask-Login:
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# ADD user_loader:
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ADD new routes:
@app.route('/register', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
@app.route('/logout')
@app.route('/profile')
@app.route('/profile/edit', methods=['GET', 'POST'])
@app.route('/user/<username>')

# UPDATE existing routes:
create_study_group() - Add @login_required, use current_user.id
join_study_group() - Add @login_required, use current_user.id
create_discussion() - Add @login_required, use current_user.id
reply_to_discussion() - Add @login_required, use current_user.id
```

### Step 3: Create New Templates 📄

#### templates/register.html
- Registration form with all fields
- Email validation (must be @princeton.edu)
- Password strength indicator
- Link to login page
- Princeton branding

#### templates/login.html
- Login form (email/username + password)
- Remember me checkbox
- Link to registration
- "Forgot password?" placeholder
- Clean, centered design

#### templates/profile.html
- User's profile information
- List of hosted study groups
- List of joined study groups
- List of discussion posts
- Total replies count
- "Edit Profile" button
- Member since date

#### templates/user_profile.html
- Public profile view
- Similar to profile.html but for other users
- No edit button
- "This is you!" message if viewing own profile

#### templates/edit_profile.html
- Edit form for profile
- Full name, class year
- Optional password change
- Cannot edit email/username (show as read-only)
- Validation and success messages

### Step 4: Update base.html 🎨
Major navigation changes:

```html
<!-- When NOT logged in: -->
<div class="nav-actions">
    <a href="{{ url_for('login') }}">Login</a>
    <a href="{{ url_for('register') }}" class="btn-primary">Register</a>
</div>

<!-- When logged in: -->
<div class="user-menu">
    <span>Hi, {{ current_user.username }}</span>
    <div class="dropdown">
        <a href="{{ url_for('profile') }}">My Profile</a>
        <a href="{{ url_for('my_study_groups') }}">My Study Groups</a>
        <a href="{{ url_for('logout') }}">Logout</a>
    </div>
</div>
```

### Step 5: Update All Existing Templates 🔧

#### course_detail.html
- Remove name field from create study group form
- Use `{{ group.host.username }}` instead of `{{ group.host_name }}`
- Make usernames clickable links to profiles
- Add login prompt for anonymous users
- Show "Join" button only if logged in

#### discussion_board.html
- Use `{{ post.author.username }}` instead of `{{ post.author_name }}`
- Make author names clickable links
- Add login prompt for anonymous users

#### discussion_post_detail.html
- Use `{{ post.author.username }}` and `{{ reply.author.username }}`
- Remove name field from reply form
- Show reply form only if logged in
- Make all usernames clickable links

#### create_study_group.html
- Remove host_name field
- Auto-populate from current_user

#### create_discussion.html
- Remove author_name field
- Auto-populate from current_user

### Step 6: Update seed_data.py 💾

```python
# ADD import:
from models import User

# ADD function to create sample users:
def seed_users():
    users_data = [
        {'email': 'jsmith26@princeton.edu', 'username': 'jsmith26',
         'full_name': 'John Smith', 'class_year': 2026, 'password': 'password123'},
        {'email': 'alee27@princeton.edu', 'username': 'alee27',
         'full_name': 'Alice Lee', 'class_year': 2027, 'password': 'password123'},
        # ... 5-8 users total
    ]

    for user_data in users_data:
        user = User(
            email=user_data['email'],
            username=user_data['username'],
            full_name=user_data['full_name'],
            class_year=user_data['class_year']
        )
        user.set_password(user_data['password'])
        db.session.add(user)
    db.session.commit()

# UPDATE seed_study_groups():
# Instead of host_name, use host_id from random user
# Instead of participant name, use user_id

# UPDATE seed_discussions():
# Instead of author_name, use author_id from random user

# Call order:
seed_users()  # FIRST!
seed_courses()
seed_study_groups()
seed_discussions()
```

### Step 7: Test Everything ✅

Test matrix:

**Anonymous Users (Not Logged In):**
- ✅ Can view home page
- ✅ Can browse courses
- ✅ Can view study groups (but not join)
- ✅ Can view discussions (but not post/reply)
- ✅ See "Login to join" prompts
- ✅ Redirected to login when trying protected actions

**Logged In Users:**
- ✅ Can register new account
- ✅ Can log in with email or username
- ✅ Can view own profile
- ✅ Can edit profile
- ✅ Can view other users' profiles
- ✅ Can create study groups (no name field)
- ✅ Can join study groups (no name prompt)
- ✅ Can create discussions (no name field)
- ✅ Can reply to discussions (no name field)
- ✅ See own username throughout app
- ✅ Can click usernames to view profiles
- ✅ Can logout

**Data Integrity:**
- ✅ Passwords are hashed (never plaintext)
- ✅ Email must be @princeton.edu
- ✅ Usernames are unique
- ✅ User activity is tracked correctly
- ✅ Foreign key relationships work

## Sample User Credentials (For Testing)

After running seed script, you can login with:

```
Email: jsmith26@princeton.edu
Username: jsmith26
Password: password123

Email: alee27@princeton.edu
Username: alee27
Password: password123

(etc... for all seeded users)
```

## Implementation Time Estimate

- Step 1 (forms.py): 30 minutes
- Step 2 (app.py): 1 hour
- Step 3 (new templates): 1.5 hours
- Step 4 (base.html): 30 minutes
- Step 5 (update templates): 1 hour
- Step 6 (seed_data.py): 45 minutes
- Step 7 (testing): 45 minutes

**Total: ~6 hours**

## Current Progress

- ✅ Planning complete
- ✅ Requirements updated
- ✅ Packages installed
- ✅ Models updated
- ⏳ Forms (Step 1)
- ⏳ Routes (Step 2)
- ⏳ Templates (Steps 3-5)
- ⏳ Seed data (Step 6)
- ⏳ Testing (Step 7)

## Questions to Consider

1. **Password Reset**: Do you want "Forgot Password" functionality? (adds complexity)
2. **Email Verification**: Should emails be verified? (requires email sending)
3. **Remember Me**: How long should "remember me" sessions last?
4. **Profile Pictures**: Use initials in colored circles or allow uploads?
5. **Privacy**: Should profiles be public or require login to view?

## Recommended Approach

**Option A: Do it all now** (6 hours)
- Complete implementation
- Test thoroughly
- Have fully working auth system

**Option B: Incremental** (spread over time)
- Do Step 1 (forms)
- Do Step 2 (routes)
- Test basic login/register
- Then do remaining steps

**Option C: I continue** (you review/test)
- I implement all steps
- You test and provide feedback
- We fix any issues together

Which approach would you prefer?
