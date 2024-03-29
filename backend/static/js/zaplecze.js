$(document).ready(function() {
    // Select sliders and value elements 
    const cat_slider = $("#CatSlider");
    const cat_value = $("#CatSliderValue");
    const scat_slider = $("#SubCatSlider");
    const scat_value = $("#SubCatSliderValue");

    // Add an input event listener 
    cat_slider.on('input', function() {
        cat_value.val(cat_slider.val());
    });

    scat_slider.on('input', function() {
        scat_value.val(scat_slider.val());
    });


    $('#catForm').on('submit', function(event) {
        event.preventDefault(); // Prevent form from submitting normally
        
        // Serialize form data
        const formData = $(this).serialize();
        const cardId = $('#main').data('card-id');

        // Check if any field is empty
        let emptyFields = false;
        $(this).find('input').each(function() {
            if ($(this).val() === '') {
                emptyFields = true;
                return false; // Exit the loop early
            }
        });
        
        if (emptyFields) {
            alert('Please fill in all fields.');
            return; // Do not proceed with submission
        }
        
        if ($("input#topic").val()){
            //PUT request to update DB
            $.ajax({
                type: 'PUT',
                url: '/api/' + cardId + '/',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                },
                data: {"topic": $("input#topic").val()},
                success: function(response) {
                    console.log(response);
                },
                error: function(error) {
                    // Handle error response here
                    if(error.responseJSON.data){
                        $("div#class_spinner").parent().append("<p>An error ocurred: "+error.responseJSON.data+"</p>");
                    } else {
                        $("div#class_spinner").parent().append("<p>An error ocurred: "+error.responseJSON.detail+"</p>");
                    }
                    $("div#class_spinner").remove();
                    console.error(error);
                }
            })
        }

        const spin = document.createElement("div");
        spin.setAttribute("id", "class_spinner");
        spin.classList.add("spinner");
        $(this).parent().append(spin);
        $(this).remove();

        // Send POST request
        $.ajax({
            type: 'POST',
            url: '/api/structure/'+ cardId +'/',
            data: formData,
            success: function(response) {
                const fragment = document.createDocumentFragment();
                fragment
                    .appendChild(document.createElement("h3"))
                    .textContent = "Utworzono kategorie";
                const ul = document.createElement("ul");
                Object.keys(response.data).forEach((e) => {
                    const li = document.createElement("li");
                    li.textContent = e;
                    const inner_ul = document.createElement("ul");
                    response.data[e].forEach((i) => {
                        const inner_li = document.createElement("li");
                        inner_li.textContent = i;
                        inner_ul.appendChild(inner_li);
                    });
                    li.appendChild(inner_ul);
                    ul.appendChild(li);
                })
                fragment.appendChild(ul);
                $("div#class_spinner").parent().append(fragment);
                $("div#class_spinner").parent().append("<p>Tokens used: "+response.tokens+"</p>");
                $("div#class_spinner").parent().append("<p>Estimated cost: "+response.cost+"USD</p>");
                $("div#class_spinner").remove();
            },
            error: function(error) {
                // Handle error response here
                try{
                    $("div#class_spinner").parent().append("<p>An error ocurred: "+error.responseJSON.data+"</p>");
                } catch {
                    $("div#class_spinner").parent().append("<p>An error ocurred: "+error.responseJSON.detail+"</p>");
                }
                $("div#class_spinner").remove();
                console.error(error);
            }
        });
    });
});