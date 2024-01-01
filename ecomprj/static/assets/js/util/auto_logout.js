var countdownSeconds = null
var countdownTimeout

function resetCountdown(){
    try{
        $('#overlay').fadeOut();
        if(autoLogoutTime != 'undefined' && autoLogoutTime != null && !Number.isNaN(autoLogoutTime)){
            isReset = true;
            countdownSeconds = autoLogoutTime;
            clearTimeout(countdownTimeout);
            call_reset_session_timeout_command();
            updateCountdown();
        }
    }catch (error) {
        console.error('An error occurred:', error.message);
    }

}


function updateCountdown() {
    if(countdownSeconds!=null){
        try{
            var minutes = Math.floor(countdownSeconds / 60);
            var seconds = countdownSeconds % 60;

            if(countdownSeconds > 0 && countdownSeconds <= 60 && document.getElementById('countdown-display')!=null){
                document.getElementById('countdown-display').innerHTML = minutes + ':' + (Math.round(seconds) < 10 ? '0' : '') + Math.round(seconds);
                $('#overlay').fadeIn();
            }


            if (countdownSeconds > 0) {
                countdownSeconds--;
                call_reset_session_timeout_command();
                countdownTimeout = setTimeout(updateCountdown, 1000);
            }
            else{
                logoff('Y');
            }

        }catch(error){
            console.error('An error occurred:', error.message);
        }
    }
    else{
        console.error('countdownSeconds is obtained as null');
    }
}


