function validateForm() {
    var Name = document.getElementById("Name").value;
    var email = document.getElementById("email").value;
    var phone = document.getElementById("phone").value;
    var serviceType = document.querySelectorAll('input[name="serviceType"]:checked');
    var reference = document.getElementById("reference").value;
    var emailRegex = /^[A-Za-z0-9._%-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}$/;

    if (Name ==""){
           alert("Full Name must be filled out");
           return false;
    }

    if(email ==""){
           alert("Email must be filled out");
           return false;
    }else if (!emailRegex.test(email)) {
            alert("Invalid email format");
            return false;
    }


    if (phone ==""){
            alert("Phone must be filled out");
            return false;
    }
    if (serviceType.length === 0) {
            alert("Please select at least one interest");
            return false;
    }
    if (reference === "") {
            alert("Please select a Satisfactory standard ");
            return false;
    }
    
    
    return true;
}