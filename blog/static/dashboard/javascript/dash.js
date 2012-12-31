$(document).ready(function(){

    function checkAuthorized(){
        return $.ajax({
            type: 'GET',
            url: '/checkpocket',
            data: {}
        });
    };

    function pocketAuthorization(){
        // $.ajax({
        //     type: 'GET',
        //     url: '/pocket',
        //     data: {}
        // });
        window.location.href='/pocket'
    };

    function getArticles(){
        $.ajax({
            type: 'GET',
            url: '/getarticles',
            data: {},
            success: function(response){
                $('.content').append(response);
            }
        })

    };

    function getAuthorized(authorized){
        authorized.success(function(isAuthorized){
            switch(isAuthorized){
                case 'False':
                    pocketAuthorization();

                case 'True':
                    articleList = getArticles();
            }
        })
    };

    

    var authorized = checkAuthorized();

    getAuthorized(authorized);

    $('#addItem').click(function(){
        $('#todoContent').prepend('<div class="todoItem" id="newItem"><input type="text" id="addTodo"><button id="submitTodo">&#x2713</button></div>');
        $('#addTodo').focus();
    });

    $('#submitTodo').live('click', function(){
        var item = $('#addTodo').val()
        $.ajax({
            type: 'GET',
            url: '/addtodo',
            data: {'item': item},
            success: function(response){
                $("#newItem").remove();
                $("#todoContent").prepend(response);
            }
        })
    });

    $("#newItem").live('keyup', function(e){
        if(e.keyCode == 13){
            $('#submitTodo').click();
        }
    });

    $('.deleteItem').live('click',function(){
        id = this.id;
        $.ajax({
            type:'GET',
            url: '/deletetodo',
            data: {'id': id},
            success: function(response){
                $('.todoItem#' + id).remove();
            }
        })
    })
});
