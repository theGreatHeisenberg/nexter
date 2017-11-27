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
$(document).ready(function(){
    var handle = $.cookie('handle');
    // if (!handle) {
    //     window.location.href = '/initializr/login.html';
    // }
    google.books.load();
    $("#loader").removeClass("hidden");
    window.setTimeout(function(){render_books("achillesHeelV2")}, 4000);
});
function render_books(handle) {
    $.ajax({
        url: "http://192.168.56.101:8000/data/" + handle,
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
function get_book_div(author, title, image_url, isbn, id) {
    return '<div class="card col-sm-4 book-container"><img class="card-img-top col-sm-6 book-image" src="__URL__" alt="Card image cap"><div class="card-body col-sm-6"><h4 class="card-title book-title"><a href="https://www.goodreads.com/book/show/__ID__" class="card-title book-title">__TITLE__</a></h4><p class="card-text author-title">by __AUTHOR__</p><a href="#" data-id = "__ISBN__" data-toggle="modal" data-target="#exampleModalLong" class="preview-link">preview</a></div></div>'.replace("__URL__", image_url).replace("__AUTHOR__",author).replace("__TITLE__", title).replace("__ISBN__",isbn).replace("__ID__", id);
}
// $('#exampleModalLong').on('shown.bs.modal', function (e) {
//     load_book();
// })
$(document).on("click", ".preview-link", function () {
    var myBookId = $(this).data('id');
    console.log("loading: " + myBookId);
    load_book(myBookId)
});
function load_book(isbn) {
    var viewer = new google.books.DefaultViewer(document.getElementById('viewerCanvas'));
    viewer.load('ISBN:' + isbn);
}