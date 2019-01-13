// Base Form Class Declaration
class Input{
    constructor(id){
        this._id = id;
        this._dom = $('input#'+id);
        this._errorField = $('#'+id+'_error');
        this._name = this._dom.attr('name');
    }

    add_error(messageArray){
        var message = "";
        $.each(messageArray, function (key, element) {
            message += element+"<br>";
        });
        this._errorField.append(message);
        this._errorField.css('display', 'block');
    }

    reset_error(){
        this._errorField.html('');
        this._errorField.css('display','none');
    }

    get name(){
        return this._name;
    }
}


class Form{
    constructor(cls){
        cls = '.' + cls;

        this._class = cls;
        this._form = $('form'+cls);
        this._inputs = this.generate_inputs();
        this._submitBtn = $(cls+'SubmitButton');
        this._defaultBtnText = this.submitBtn.html();
        this._submissionUrl = this.form.attr('action');
    }

    generate_inputs(){
        var inputs = [];
        const dom = $(this._class+' :input');
        $.each(dom, function () {
            if(this.id){
                const inputDom = new Input(this.id);
                inputs.push(inputDom);
            }
        });
        return inputs;
    }

    reset_form_errors(){
        $.each(this._inputs, function () {
            this.reset_error();
        });
    }

    add_errors(error){   //error argument is default django form validation error response: form.errors
        $.each(this._inputs, function () {
            if(error.hasOwnProperty(this.name)){
               this.add_error(error[this.name]);
            }
        });
    }

    get_data(){
        return this.form.serialize();
    }

    update_btn_text(text){
        this.submitBtn.html(text);
    }

    submit(event){
        event.preventDefault();
        this.reset_form_errors();
        this.update_btn_text('Validating Information');
        const form = this;

        $.ajax({
            url: this.submissionUrl,
            method: 'POST',
            data: this.get_data(),
            cache: false,
            success: function(response){
                form.submission_success(response);
            },
            error: function (message) {
                form.log_error(message);
            }
        });
    }

    submission_success(response){
        if(response.hasOwnProperty('message')){
            this.update_btn_text(response['message']);
        } else {
            this.update_btn_text(this.defaultBtnText);
        }
        const status = response['status'];
        if(status === false){
            const error = response['error'];
            this.add_errors(error);
        } else if (status === true){
            this.form[0].reset();
        }

        if(response.hasOwnProperty('redirect_url')){
            window.open(response['redirect_url'], '_self');
        }
    }

    log_error(message){
        this.update_btn_text('Server Error. Please Try Again Later.');
        alert(message);
        console.log(message);
    }

    get form(){
        return this._form;
    }

    get class(){
        return this._class;
    }

    get inputs(){
        return this._inputs;
    }

    get submitBtn(){
        return this._submitBtn;
    }

    get defaultBtnText(){
        return this._defaultBtnText;
    }

    get submissionUrl(){
        return this._submissionUrl;
    }
}

const registerFormClass = 'registerForm';
let registerForm = new Form(registerFormClass);


registerForm.form.submit(function (event) {
    event.preventDefault();
    registerForm.submit(event);
});

const loginFormClass = 'loginForm';
let loginForm = new Form(loginFormClass);


loginForm.form.submit(function (event) {
    event.preventDefault();
    loginForm.submit(event);
});
