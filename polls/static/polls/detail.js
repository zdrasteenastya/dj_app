function checkChoice(){
questions = document.getElementsByClassName('question')
    if($('input:radio:checked').length < questions.length ){
        alert('NOT SELECT');
    }
    else {
    console.log('someday page will be reload')
    }
}

