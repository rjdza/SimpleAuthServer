
def login():
    return(LOGIN_BODY)

def auth():
    RET = AUTH_BODY
    RET=RET.replace("$$AUTHRES$$", "Authentication Results")
    return(RET)

LOGIN_FORM='''
 <form action="action_page.php" method="post">
  <div class="imgcontainer">
    <img src="https://www.w3schools.com/howto/img_avatar2.png" alt="Avatar" class="avatar">
  </div>

  <div class="container">
    <label for="uname"><b>Username</b></label>
    <input type="text" placeholder="Enter Username" name="uname" required>

    <label for="psw"><b>Password</b></label>
    <input type="password" placeholder="Enter Password" name="psw" required>

    <button type="submit">Login</button>
    <label>
      <input type="checkbox" checked="checked" name="remember"> Remember me
    </label>
  </div>

  <div class="container" style="background-color:#f1f1f1">
    <button type="button" class="cancelbtn">Cancel</button>
    <span class="psw">Forgot <a href="#">password?</a></span>
  </div>
</form> 
'''

LOGIN_BODY = '''
<h2>Ingress Security Authentication Services</h2>

<div id="id01" class="modal_visible">

  <form class="modal-content animate" action="/authenticate" method="post">
    <div class="imgcontainer">
      <img src="img/cropped-Ingress-tech-3.png" alt="Ingress Technology" class="avatar-full">
    </div>

    <div class="container">
      <label for="email"><b>Email Address</b></label>
      <input type="text" placeholder="Enter Email Address" name="email" required>

      <label for="password"><b>Password</b></label>
      <input type="password" placeholder="Enter Password" name="password" required>

      <button type="submit">Login</button>
      <label>
        <input type="checkbox" checked="checked" name="remember"> Remember me
      </label>
    </div>

    <div class="container" style="background-color:#f1f1f1">
      <button type="button" onclick="document.getElementById('id01').style.display='none'" class="cancelbtn">Cancel</button>
      <span class="psw">Forgot <a href="#">password?</a></span>
    </div>
  </form>
</div>

<script>
// Get the modal
var modal = document.getElementById('id01');

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}
</script>
'''


LOGIN_BODY_BAK = '''
<h2>Modal Login Form</h2>

<button onclick="document.getElementById('id01').style.display='block'" style="width:auto;">Login</button>

<div id="id01" class="modal">

  <form class="modal-content animate" action="/action_page.php" method="post">
    <div class="imgcontainer">
      <span onclick="document.getElementById('id01').style.display='none'" class="close" title="Close Modal">&times;</span>
      <img src="https://www.w3schools.com/howto/img_avatar2.png" alt="Avatar" class="avatar">
    </div>

    <div class="container">
      <label for="uname"><b>Email Address</b></label>
      <input type="text" placeholder="Enter Email Address" name="uname" required>

      <label for="psw"><b>Password</b></label>
      <input type="password" placeholder="Enter Password" name="psw" required>

      <button type="submit">Login</button>
      <label>
        <input type="checkbox" checked="checked" name="remember"> Remember me
      </label>
    </div>

    <div class="container" style="background-color:#f1f1f1">
      <button type="button" onclick="document.getElementById('id01').style.display='none'" class="cancelbtn">Cancel</button>
      <span class="psw">Forgot <a href="#">password?</a></span>
    </div>
  </form>
</div>

<script>
// Get the modal
var modal = document.getElementById('id01');

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}
</script>
'''

AUTH_BODY = '''
<h2>Ingress Security Authentication Services</h2>

<div id="id01" class="modal_visible">
  <div class="modal-content animate">
    <div class="imgcontainer">
      <img src="img/cropped-Ingress-tech-3.png" alt="Ingress Technology" class="avatar-full">
    </div>

    <div class="container">
    $$AUTHRES$$
    </div>
  </div>
</div>

<script>
// Get the modal
var modal = document.getElementById('id01');

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}
</script>
'''

