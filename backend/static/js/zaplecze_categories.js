$(document).ready(function() {
    // Select sliders and value elements 
    const art_slider = $("#ArtSlider");
    const art_value = $("#ArtSliderValue");
    const p_slider = $("#ParagraphsSlider");
    const p_value = $("#ParagraphsSliderValue");
    const d_slider = $("#DaysSlider");
    const d_value = $("#DaysSliderValue");

    // Add an input event listener 
    art_slider.on('input', function() {
        art_value.val(art_slider.val());
    });

    p_slider.on('input', function() {
        p_value.val(p_slider.val());
    });

    d_slider.on('input', function() {
        d_value.val(d_slider.val());
    });

    const today = new Date();
    let dd = today.getDate();
    let mm = today.getMonth() + 1;
    let yyyy = today.getFullYear();
    dd < 10 ? dd = '0' + dd : null;
    mm < 10 ? mm = '0' + mm : null; 
    document.getElementById("start_date").setAttribute("value", yyyy + '-' + mm + '-' + dd);

    $("button#categories").on('click', (event) => {
        const cardId = $('#main').data('card-id');
        $.ajax({
            type: 'GET',
            url: '/api/structure/'+ cardId +'/',
            success: (response) => {
                $("#cat_table").parent().show();
                response.sort((a,b) => a.parent - b.parent);
                parents = {};
                $("#cat_table>tbody").empty();
                response.forEach(e => {
                    e.parent == 0 ? parents[e.id] = e.name : null;
                    const fragment = document.createDocumentFragment()
                        .appendChild(document.createElement("tr"));
                    const check = document.createElement("input");
                    check.type = "checkbox";
                    check.id = e.id;
                    check.name = e.name;
                    check.checked = false;
                    fragment
                        .appendChild(document.createElement("td"))
                        .appendChild(check);
                    fragment
                        .appendChild(document.createElement("td"))
                        .textContent = e.parent==0 ? e.name : parents[e.parent]+' -> '+e.name;
                    $("#cat_table>tbody").append(fragment);
                });
                $("button#categories").remove();
                $("#articles").show();
                if (response.length != $("#wp_post_count").innerHTML){
                    $.ajax({
                        type: 'PUT',
                        url: '/api/' + cardId + '/',
                        headers: {
                            'X-CSRFToken': getCookie('csrftoken')
                        },
                        data: {"wp_post_count": response.length}
                    });
                }
            },
            error: (e) => {
                console.error(e)
            }
        });
    });
    $("#articles").on('click', function(event) {
        const ul = document.createElement("ul");
        ul.setAttribute("id", "selected_cats")
        const rows = document.getElementById("cat_table").getElementsByTagName("tr");
        for (let i = 0; i < rows.length; i++) {
            const checkbox = rows[i].getElementsByTagName("input")[0];
            if (checkbox && checkbox.type === "checkbox" && checkbox.checked) {
                const rowData = rows[i].textContent.trim();
                li = document.createElement("li");
                li.textContent = rowData;
                li.setAttribute("data-id", checkbox.id);
                li.setAttribute("data-name", checkbox.name);
                li.append(document.createElement("ul"))
                ul.append(li);
            }
        }
        $(this).parent().append(ul);
        $("#cat_table").parent().remove();
        $(this).remove();
        $("#writeForm").show();
    });

    $("#writeForm").on('submit', function(event) {
        event.preventDefault();
        let formData = $(this).serialize();
        const cardId = $('#main').data('card-id');
        const cats = document.getElementById("selected_cats").getElementsByTagName("li");

        const spin = document.createElement("div");
        spin.classList.add("spinner");
        $(this).parent().append(spin);
        $(this).remove();
        let data = [];
        for (i of cats) {
            let cat_data = {};
            cat_data['id'] = i.getAttribute("data-id");
            cat_data['name'] = i.getAttribute("data-name");
            data.push(cat_data);
            last_id = cat_data['id'];
        }
        
        formData += "&categories="+JSON.stringify(data);
        $.ajax({
            type: 'POST',
            url: '/api/write/'+ cardId +'/',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            },
            data: formData,
            success: function(response) {
                for (const [id, urls] of Object.entries(JSON.parse(response))) {
                    urls.forEach(function(e){
                        $("#selected_cats > [data-id=\'"+id+"\'] > ul")
                        .append("<li><a href=\""+e+"\">"+e+"</a></li>");
                        id == last_id ? $("div.spinner").remove() : null;
                    })
                }
            },
            error: function(response) {
                console.error(response);
            }
        })
    });
});