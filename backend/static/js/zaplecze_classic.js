function updateRGB(value) {
             
    var r = parseInt(value.substring(1, 3), 16);
    var g = parseInt(value.substring(3, 5), 16);
    var b = parseInt(value.substring(5, 7), 16);
    var rgbValue = r + "," + g + "," + b;
    $('#rgbValue').val(rgbValue);

    console.log(rgbValue);
}

$(document).ready(function() {
    var cardId = $('#classic_main').data('card-id');

    $('button[type="submit_tsv"]').on('click', function(event) {
        event.preventDefault();
        console.log('Zaliczyło!');
        
        var colorValue = $('#rgbValue').val();

        const data = {
            tsvInput: $('#tsvInput').val(),
            graphicSource: $('input[name="graphicSource"]:checked').val(),
            overlayOption: $('input[name="overlayOption"]:checked').val(),
            dateInput: $('#dateInput').val(),
            publishInterval: $('#publishInterval').val(),
            openai_api_key: $('#openai_api_key_classic').val(),
            faqOption: $('input[name="faqOption"]:checked').val(),
            overlayColor: colorValue
        };


        $.ajax({
            url: '/api/create/' + cardId + '/zaplecze_classic/',
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            data: JSON.stringify(data),
            success: function(response) {
                console.log(response);
                
            },
            error: function(error) {
                console.error('Error:', error);
            }
        });
    });

    function getWordpressPostsTitles() {

        const password = document.getElementById('wp_api_key').innerText;
        const domain = document.getElementById('domain').innerText;
        const login = document.getElementById('wp_user').innerText;
      
        const token = btoa(`${login}:${password}`);
        const authHeader = { 'Authorization': `Basic ${token}` };
      
        const apiUrl = `https://${domain}/wp-json/wp/v2/posts`;
        console.log(apiUrl);
      
        fetch(apiUrl, { headers: authHeader })
          .then(response => {
            if (!response.ok) {
              throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
          })
          .then(posts => {
            console.log('Tytuły wpisów:');
            posts.forEach(post => {
              console.log(post.title.rendered);
            });
          })
          .catch(error => {
            console.error('Wystąpił błąd podczas pobierania wpisów:', error);
          });
      }
      
      setInterval(getWordpressPostsTitles, 600000);

    

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = $.trim(cookies[i]);
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
