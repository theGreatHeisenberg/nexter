var sample_books = {
    "twitter_handle": "shreyas",
    "recommendations": [
        {
            "book_id": 1953,
            "title": "Tale of Two cities",
            "author": "Charles Dickens",
            "original_publication_year": "1935",
            "ratings": 4.2,
            "confidence_score": 78,
            "isbn":"9780486417769",
            "image_url": "https://images.gr-assets.com/books/1344922523l/1953.jpg"
        },
        {
            "book_id": 2657,
            "title": "To Kill a Mockingbird",
            "author": "Harper Lee",
            "original_publication_year": "1935",
            "ratings": 4.2,
            "confidence_score": 78,
            "isbn":"0061980269",
            "image_url": "https://images.gr-assets.com/books/1361975680l/2657.jpg"
        }
    ]
}
handle_global = "";
$(document).ready(function(){
    var handle = $.cookie('handle');
    // if (!handle) {
    //     window.location.href = '/initializr/login.html';
    // }
    google.books.load();
    $("#loader").removeClass("hidden");
    $("#loader-related").removeClass("hidden");
    $('#search').on('click', function (e) {
        e.preventDefault(); // disable the default form submit event
        console.log("clicked search");
        $('.single-item').empty();
        if (! ($("#handle_input").val())){
            $("#error_user").removeClass("hidden")
            return
        }
        else {
            register_user($("#handle_input").val(), function () {
                $("#main_container").removeClass("hidden");
                window.setTimeout(function(){render_books($("#handle_input").val())}, 2000);
                window.setTimeout(function(){render_related_books($("#handle_input").val())}, 2000);
            })
        }
    });

});
function render_books(handle) {
    $.ajax({
        url: "http://192.168.56.101:8000/nexterApi/recommendations/" + handle,
        type: 'GET',
        success: function(res) {
            console.log(res);
            sample_books = res;
            var recommendations = sample_books["recommendations"];
            $("#loader").addClass("hidden");
            for(var i =0; i < recommendations.length; i++)
            {
                var x = i;
                $('.single-item').append(get_book_div(recommendations[x]["author"], recommendations[x]["title"], recommendations[x]["image_url"], recommendations[x]["isbn"], recommendations[x]["book_id"]))
            }
            $(".single-item").slick({
                dots: true,
                infinite: false,
                slidesToShow: 4,
                slidesToScroll: 3
            });
            if (recommendations.length <= 0)
            {
                $("#emptyview").removeClass("hidden");
            }
            else
            {
                $("#emptyview").addClass("hidden");
            }
        }
    });
}
function render_related_books(handle) {
    $.ajax({
        url: "http://192.168.56.101:8000/nexterApi/relatedBooks/" + handle,
        type: 'GET',
        success: function(res) {
            console.log(res);
            sample_books = res;
            var recommendations = sample_books["recommendations"];
            $("#loader-related").addClass("hidden");
            for(var i =0; i < recommendations.length; i++)
            {
                var x = i;
                $('.single-item-related').append(get_book_div(recommendations[x]["author"], recommendations[x]["title"], recommendations[x]["image_url"], recommendations[x]["isbn"], recommendations[x]["book_id"]))
            }
            try
            {
                $(".single-item-related").slick('unslick');
            }
            catch(e)
            {
                console.log("prevent page from breaking")
            }
            setTimeout( function(){$(".single-item-related").slick({
                dots: true,
                infinite: false,
                slidesToShow: 4,
                slidesToScroll: 3
            })}, 100);
            if (recommendations.length <= 0)
            {
                $("#emptyview-related").removeClass("hidden");
            }
            else
            {
                $("#emptyview-related").addClass("hidden");
            }
        }
    });
}
function get_book_div(author, title, image_url, isbn, id) {
    return '<div class="card col-sm-4 book-container"><img class="card-img-top col-sm-6 book-image" src="__URL__" alt="Card image cap"><div class="card-body col-sm-6"><h4 class="card-title book-title"><a href="https://www.goodreads.com/book/show/__ID__" class="card-title book-title">__TITLE__</a></h4><p class="card-text author-title">by __AUTHOR__</p><a id="preview-link" href="#" data-id = "__ISBN__" data-toggle="modal" data-target="#exampleModalLong" class="preview-link">preview</a><p><a id="feedback" class="preview-link" data-id="__ID__" tabindex="0">Interested ✓ </a></p></div></div>'.replace("__URL__", image_url).replace("__AUTHOR__",author).replace("__TITLE__", title).replace("__ISBN__",isbn).replace(/__ID__/g, id);
}
// $('#exampleModalLong').on('shown.bs.modal', function (e) {
//     load_book();
// })
$(document).on("click", "#preview-link", function () {
    var myBookId = $(this).data('id');
    console.log("loading: " + myBookId);
    load_book(myBookId)
});
$(document).on("click", "#feedback", function () {
    var myBookId = $(this).data('id');
    console.log("loading: " + myBookId);
    post_feedback(myBookId, function () {
        $('.single-item-related').empty();
        render_related_books(handle_global)
    });
});
function load_book(isbn) {
    var viewer = new google.books.DefaultViewer(document.getElementById('viewerCanvas'));
    viewer.load('ISBN:' + isbn);
}

function post_feedback(book_id, callback) {
    $.ajax({
        url: "http://192.168.56.101:8000/nexterApi/feedback",
        type: 'POST',
        contentType:"application/json",
        data:JSON.stringify({"twitter_handle": handle_global, "book_id": book_id, "feedback":true}),
        success: function(res) {
            console.log(res);
            $("#loader-related").removeClass("hidden");
            setTimeout(function(){callback()}, 10);
        }
    });
}

function register_user(handle, callback) {
    handle_global = handle;
    $.ajax({
        url: "http://192.168.56.101:8000/nexterApi/user/" + handle,
        type: 'GET',
        success: function(res) {
            console.log(res);
            callback();
        },
        error: function (res) {
            $("#error_user").removeClass("hidden")
        }
    });
}