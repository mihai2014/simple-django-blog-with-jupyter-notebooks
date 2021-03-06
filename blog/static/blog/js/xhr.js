var DEBUG = true;

err_codes = {
'100':['Continue' ,'information','The server has received the request headers, and the client should proceed to send the request body'],
'101':['Switching Protocols' ,'information','The requester has asked the server to switch protocols'],
'103':['Checkpoint' ,'information','Used in the resumable requests proposal to resume aborted PUT or POST requests'],
'200':['OK' ,'successful','The request is OK (this is the standard response for successful HTTP requests)'],
'201':['Created' ,'successful','The request has been fulfilled, and a new resource is created'],
'202':['Accepted' ,'successful','The request has been accepted for processing, but the processing has not been completed'],
'203':['Non-Authoritative Information' ,'successful','The request has been successfully processed, but is returning information that may be from another source'],
'204':['No Content' ,'successful','The request has been successfully processed, but is not returning any content'],
'205':['Reset Content' ,'successful','The request has been successfully processed, but is not returning any content', 'and requires that the requester reset the document view'],
'206':['Partial Content' ,'successful','The server is delivering only part of the resource due to a range header sent by the client'],
'300':['Multiple Choices' ,'redirection','A link list. The user can select a link and go to that location. Maximum five addresses'],
'301':['Moved Permanently' ,'redirection','The requested page has moved to a new URL'], 
'302':['Found' ,'redirection','The requested page has moved temporarily to a new URL'], 
'303':['See Other' ,'redirection','The requested page can be found under a different URL'],
'304':['Not Modified' ,'redirection','Indicates the requested page has not been modified since last requested'],
'306':['Switch Proxy' ,'redirection','No longer used'],
'307':['Temporary Redirect' ,'redirection','The requested page has moved temporarily to a new URL'],
'308':['Resume Incomplete' ,'redirection','Used in the resumable requests proposal to resume aborted PUT or POST requests'],
'400':['Bad Request' ,'client error','The request cannot be fulfilled due to bad syntax'],
'401':['Unauthorized' ,'client error','The request was a legal request, but the server is refusing to respond to it. For use when authentication is possible but has failed or not yet been provided'],
'402':['Payment Required' ,'client error','Reserved for future use'],
'403':['Forbidden' ,'client error','The request was a legal request, but the server is refusing to respond to it'],
'404':['Not Found' ,'client error','The requested page could not be found but may be available again in the future'],
'405':['Method Not Allowed' ,'client error','A request was made of a page using a request method not supported by that page'],
'406':['Not Acceptable' ,'client error','The server can only generate a response that is not accepted by the client'],
'407':['Proxy Authentication Required' ,'client error','The client must first authenticate itself with the proxy'],
'408':['Request Timeout' ,'client error','The server timed out waiting for the request'],
'409':['Conflict' ,'client error','The request could not be completed because of a conflict in the request'],
'410':['Gone' ,'client error','The requested page is no longer available'],
'411':['Length Required' ,'client error','The "Content-Length" is not defined. The server will not accept the request without it'],
'412':['Precondition Failed' ,'client error','The precondition given in the request evaluated to false by the server'],
'413':['Request Entity Too Large' ,'client error','The server will not accept the request, because the request entity is too large'],
'414':['Request-URI Too Long' ,'client error','The server will not accept the request, because the URL is too long. Occurs when you convert a POST request to a GET request with a long query information'],
'415':['Unsupported Media Type' ,'client error','The server will not accept the request, because the media type is not supported'],
'416':['Requested Range Not Satisfiable' ,'client error','The client has asked for a portion of the file, but the server cannot supply that portion'],
'417':['Expectation Failed' ,'client error','The server cannot meet the requirements of the Expect request-header field'],
'500':['Internal Server Error' ,'sever error','A generic error message, given when no more specific message is suitable'],
'501':['Not Implemented' ,'sever error','The server either does not recognize the request method, or it lacks the ability to fulfill the request'],
'502':['Bad Gateway' ,'sever error','The server was acting as a gateway or proxy and received an invalid response from the upstream server'],
'503':['Service Unavailable' ,'sever error','The server is currently unavailable (overloaded or down)'],
'504':['Gateway Timeout' ,'sever error','The server was acting as a gateway or proxy and did not receive a timely response from the upstream server'],
'505':['HTTP Version Not Supported' ,'sever error','The server does not support the HTTP protocol version used in the request'],
'511':['Network Authentication Required' ,'sever error','The client needs to authenticate to gain network access']
}

function getErr(status){
    var err_name = err_codes[status][0];
    var err_state = err_codes[status][1];
    var fullDescription = err_codes[status][2];
    var errMsg = "Error " + status + " : " + err_name + "\n[" + err_state + " - " + fullDescription+"]";
    return errMsg;
}

debug = function(xhr){
            if(DEBUG){
                var errMsg = getErr(xhr.status);
                ok = confirm(errMsg);
                if(!ok) return;
                html = xhr.responseText;
                var debugwindow = window.open("", "", "resizable=yes");
                debugwindow.document.write(html);
            }else{
                alert("Error "+xhr.status);
            }
        }

debug0 = function(xhr){
                html = xhr.responseText;
                var debugwindow = window.open("", "", "resizable=yes");
                debugwindow.document.write(html);
        }

function getXHR(){
    var xhr = false;
    if (window.XMLHttpRequest) {
        xhr = new XMLHttpRequest();
    } else { //code for IE6, IE5
        xhr = new ActiveXObject("Microsoft.XMLHTTP");
    }
    return xhr;
}

read_csrf = function(){
    /****  include  in template  ****/
    var csrf_token = document.getElementsByName("csrfmiddlewaretoken")[0].value;
    /****  render csrf in views.py  ****/
    //var csrf_token = "{{ csrf_token }}"
    return csrf_token;
}

/*
xhr.onreadystatechange = function () {
    if (xhr.readyState < 4){
        //0 - UNSENT (object constructed)
        //1 - OPENED (open successfully)
        //2 - HEADERS_RECEIVED (redirects and headers received)
        //3 - LOADING (response body)
        //4 - DONE (transfer complete or error)
    }
    else if (xhr.readyState === 4) {
        
        if (xhr.status == 200 && xhr.status < 300){
            alert(xhr.responseText);
        }
        else{
            alert(xhr.status);
        }
    }
}

xhr.onload = function() {
    if (xhr.status === 200){
        alert(xhr.responseText);
    }
    else{
        alert(xhr.status);
    }
}

xhr.onerror = function() {
    alert("Error: No response from server.");
}

xhr.open('GET', url);
xhr.send(null);
xhr.open('POST', url);
xhr.send(data);
*/
