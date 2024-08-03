
window.alert = function(message, timeout=null){
  const alert = document.createElement('div');
  const alertButton = document.createElement('button');
  alertButton.innerText = 'OK';
  alert.classList.add('alert');
  alert.setAttribute('style',
 `position:fixed;
  top:180px;
  left:20%;
  padding:20px;
  border-radius:8px;
  box-shadow:0 10px 5px 0 #00000022;
  background: white;
  display:flex;
  flex-direction:column;
  border: 1px solid #333;
  transform: transformX(-50%);
  `);

  alertButton.setAttribute('style',
  `border:1px; solid #333;
   background: black;
   color:white;
   border-radius: 5px;
   padding: 5px;
  `);

  alert.innerHTML = `<span style="padding:10px;">${message}</span>`;
  alert.appendChild(alertButton);
  alertButton.addEventListener('click',(e)=>{
    alert.remove();
  });
  if(timeout != null){
      setTimeout(()=>{
        alert.remove();
      },Number(timeout))
    }
    document.body.appendChild(alert);
}
