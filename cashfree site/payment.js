async function validateupi(){
  var form=document.getElementByName('form1');

  var upiid=form.document.getElementsByName("UPI ID");
  const response=await fetch('https://api.razorpay.com/v1/payments/validate/vpa',{
    Method:"POST",
    Headers: {
      'Content-Type': "application/json",
      'Authorisation':"Basic cnpwX3Rlc3RfQ0NyUjJWeGN6WjBJTm06ekhTcEVNMFRBclg1RVBhQkoxSzAxa0pW"
    }
    Body:JSON.parse({'vpa':upiid})
  })
  const data= await response.json();
  console.log(data);
  var infor=data['success'];
  if(infor==true){
             var name=data['customer_name'];
             form.document.getElementByName("UPI ID").innerHTML = "transferring to "+name;
             }
  else{
          form.document.getElementByName("UPI ID").innerHTML = "please check your upi id";
         }
}