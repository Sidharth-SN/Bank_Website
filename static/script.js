// Register Page
function disableSubmit() {
  document.getElementById("submit").disabled = true;
 }

  function activateButton(element) {

      if(element.checked) {
        document.getElementById("submit").disabled = false;
       }
       else  {
        document.getElementById("submit").disabled = true;
      }

  }


// Home Page before Login
const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]')
const popoverList = [...popoverTriggerList].map(popoverTriggerEl => new bootstrap.Popover(popoverTriggerEl))



// Loan Page
function yesnoCheck(that) 
{
    if (that.value == "personal") 
    {
        document.getElementById("rate").value = "10.50% p.a."
    }

    if (that.value == "home") 
    {
        document.getElementById("rate").value = "6.69% p.a."
    }
    
    if (that.value == "car") 
    {
        document.getElementById("rate").value = "7.00% p.a."
    }
    
    if (that.value == "gold") 
    {
        document.getElementById("rate").value = "7.04% p.a."
    }

    if (that.value == "agriculture") 
    {
        document.getElementById("rate").value = "6.05% p.a."
    }

    if (that.value == "education") 
    {
        document.getElementById("rate").value = "8.42% p.a."
    }

    if (that.value == "business") 
    {
        document.getElementById("rate").value = "14.20% p.a."
    }
}


// Deposit Page
// const alertPlaceholder = document.getElementById('liveAlertPlaceholder')

// const alert = (message, type) => {
//   const wrapper = document.createElement('div')
//   wrapper.innerHTML = [
//     `<div class="alert alert-${type} alert-dismissible" role="alert">`,
//     `   <div>${message}</div>`,
//     '   <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>',
//     '</div>'
//   ].join('')

//   alertPlaceholder.append(wrapper)
// }

// const alertTrigger = document.getElementById('liveAlertBtn')
// if (alertTrigger) {
//   alertTrigger.addEventListener('click', () => {
//     alert('Money Deposited Successfully :)', 'success')
//   })
// }