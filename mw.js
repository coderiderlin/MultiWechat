var DEBUG_FLAG = true;
function log(msg)
{
    if(DEBUG_FLAG == true){
        send({
            name: '+log',
            payload: msg
        });
        //recv('+log-ack', function () {});//.wait();
    }
};

var countCreateMutexW=0;
var countCreateMutexA=0;

var pCreateMutexA = Module.findExportByName("kernel32.dll","CreateMutexA");
var CreateMutexA=new NativeFunction(pCreateMutexA,'int',['int','bool','pointer'],'stdcall');
log("pCreateMutexA :"+pCreateMutexA);
Interceptor.replace(pCreateMutexA,new NativeCallback(function (arrt,bInit,name) {
    log("pCreateMutexA ["+name+"]: "+Memory.readAnsiString(name));
    log("countCreateMutexA:"+countCreateMutexA);
    if(countCreateMutexA++==2)return 0;
    return CreateMutexA(arrt,bInit,name);
},'int',['int','bool','pointer'],'stdcall'));

var pCreateMutexW = Module.findExportByName("kernel32.dll","CreateMutexW");
var CreateMutexW=new NativeFunction(pCreateMutexA,'int',['int','bool','pointer'],'stdcall');
log("pCreateMutexW :"+pCreateMutexA);
Interceptor.replace(pCreateMutexW,new NativeCallback(function (arrt,bInit,name) {
    log("pCreateMutexW "+Memory.readUtf8String(name));
    log("countCreateMutexW:"+countCreateMutexW);
    if(countCreateMutexW++==2)return 0;
    return CreateMutexW(arrt,bInit,name);
},'int',['int','bool','pointer'],'stdcall'));


// var pZwTerminateProcess = Module.findExportByName("ntdll.dll","ZwTerminateProcess");
// var TerminateProcess=new NativeFunction(pZwTerminateProcess,'int',['int','int'],'stdcall');
// log("pZwTerminateProcess :"+pZwTerminateProcess);
// Interceptor.replace(pZwTerminateProcess,new NativeCallback(function (hprocess,exitCode) {
//    // log("pZwTerminateProcess ");
//     return TerminateProcess(hprocess,exitCode);
// },'int',['int','int'],'stdcall'));


var pTerminateProcess = Module.findExportByName("kernel32.dll","TerminateProcess");
var TerminateProcess=new NativeFunction(pTerminateProcess,'bool',['int','int'],'stdcall');
log("pTerminateProcess :"+pTerminateProcess);
Interceptor.replace(pTerminateProcess,new NativeCallback(function (hprocess,exitCode) {
    log("pTerminateProcess "+hprocess+" "+exitCode);
    return TerminateProcess(hprocess,exitCode);
},'bool',['int','int'],'stdcall'));


var ptrExitProcess = Module.findExportByName("kernel32.dll","ExitProcess");
var ExitProcess=new NativeFunction(ptrExitProcess,'void',['int'],'stdcall');
log("ptrExitProcess :"+ptrExitProcess);
Interceptor.replace(ptrExitProcess,new NativeCallback(function (exitCode) {
    log("ptrExitProcess "+exitCode);
    return ExitProcess(exitCode);
},'void',['int'],'stdcall'));

var ptrMessageBoxA = Module.findExportByName("user32.dll","MessageBoxA");
var MessageBoxA=new NativeFunction(ptrMessageBoxA,'int',['int','pointer','pointer','int'],'stdcall');
log("ptrMessageBoxA :"+ptrMessageBoxA);
Interceptor.replace(ptrMessageBoxA,new NativeCallback(function (hwnd,pText,pTitle,type) {
    strText=Memory.readAnsiString(pText);
    strTitle=Memory.readAnsiString(pTitle);
    log("MessageBoxA "+strText+" with title "+strTitle);
    strHook=Memory.allocAnsiString("hooked!");
    return MessageBoxA(hwnd,strHook,pTitle,type);

},'int',['int','pointer','pointer','int'],'stdcall'));

var ptrMessageBoxW = Module.findExportByName("user32.dll","MessageBoxW");
var MessageBoxW=new NativeFunction(ptrMessageBoxW,'int',['int','pointer','pointer','int'],'stdcall');
log("ptrMessageBoxW :"+ptrMessageBoxW);
Interceptor.replace(ptrMessageBoxW,new NativeCallback(function (hwnd,pText,pTitle,type) {
    try{
        strText=Memory.readUtf8String(pText);
        strTitle=Memory.readUtf8String(pTitle);
        log("MessageBoxW "+strText+" with title "+strTitle);
        strHookText=Memory.allocAnsiString("text hooked!");
        strHookTitle=Memory.allocAnsiString("title hooked!");
        return MessageBoxA(hwnd,strHookText,strHookTitle,type);
    }
    catch(err)
    {
        log("MessageBoxW err: "+err.message);
        return MessageBoxA(hwnd,pText,pTitle,type);
    }
},'int',['int','pointer','pointer','int'],'stdcall'));