$(document).ready(function() {
    const catSlider = document.getElementById('CatSlider');
    const catSliderValue = document.getElementById('CatSliderValue');

    catSlider.addEventListener('input', function () {
        catSliderValue.value = catSlider.value;
    });
    const subCatSlider = document.getElementById('SubCatSlider');
    const subCatSliderValue = document.getElementById('SubCatSliderValue');

    subCatSlider.addEventListener('input', function () {
        subCatSliderValue.value = subCatSlider.value;
    });


    $('#catForm').on('submit', function(event) {
        event.preventDefault(); // Prevent form from submitting normally
        
        // Serialize form data
        var formData = $(this).serialize();
        console.log(formData);

        // Check if any field is empty
        var emptyFields = false;
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

        // Send POST request to the /api/all/ endpoint
        $.ajax({
            type: 'POST',
            url: '/api/structure/{{data.id}}/',
            data: formData,
            success: function(response) {
                // Handle success response here
                window.location.href = '/';
            },
            error: function(error) {
                // Handle error response here
                console.log(error);
            }
        });
    });

});