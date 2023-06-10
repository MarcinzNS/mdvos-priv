document.addEventListener('DOMContentLoaded', function() 
  {
    
    var themeToggle = document.getElementById('theme-toggle');
    var body = document.body;

    body.classList.add('light');
  
    themeToggle.addEventListener('click', function() {
        console.log('Kliknięto przycisk');
        body.classList.toggle('dark');
        body.classList.toggle('light');
    });
  }
);

var lista=[[50,300],[100,350],[150,400],[50,300],[100,350],[150,400],[50,300],[100,350],[150,400]];
function rozmiar_lista(){
  return lista.length*40;
}
function draw() {
      const canvas = document.getElementById("Wsparcie");
      const ctx = canvas.getContext("2d");
      const height = lista.length * 40;

      canvas.width = 700;
      canvas.height = height;

      var h = 200 - lista.length * 25;

      ctx.fillStyle = "rgb(255, 255, 255)";
      ctx.fillRect(20, 260 - h, 660, 5);
      ctx.font = "16px Arial";
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      for (var i = 0; i < 7; i++) {
          ctx.fillStyle = "rgb(200, 200, 200)";
          ctx.fillRect(49 + i * 2 * 50, 20, 3, 240 - h);
          ctx.fillRect(100 + i * 2 * 50, 20, 1, 240 - h);
          ctx.fillStyle = "rgb(20, 20, 20)";
          ctx.fillRect(48 + i * 2 * 50, 255 - h, 5, 10);
          ctx.fillText((2014 + i * 2).toString(), 32 + i * 2 * 50, 285 - h);
      }

      for (var i = 0; i < lista.length; i++) {
          var wysokosc = 230 - i * 30 - h;
          ctx.fillStyle = "rgb(24, 24, 24)";
          ctx.fillRect(lista[i][0], wysokosc, lista[i][1], 20);
      }
  }