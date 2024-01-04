const backend_endpoint: string = `/api`;
const get_current_user: string = `${backend_endpoint}/getUser`;
const sign_in_user: string = `${backend_endpoint}/signIn`;
const sign_out_user: string = `${backend_endpoint}/signOut`;
const sign_up_user: string = `${backend_endpoint}/signUp`;

interface IUserInfoResponse {
    isLoggedIn: boolean,
    username: string,
    userId: string,
    message: string
}

type LoginStatusChangeCallback = (a: LoginStatus) => void;
const IsGuestKey = "IsGuest";
const GuestTokenKey = "GuestToken";
class LoginStatus {
    isLoggedIn: boolean;
    userId: string;
    listenerers: LoginStatusChangeCallback[]

    constructor() {
        this.isLoggedIn = false;
        this.listenerers = []
        this.userId = ""
    }

    GetIdentifier() {
        return this.IsGuest()
            ? localStorage.getItem(GuestTokenKey)
            : this.userId;
    }

    DestroyGuest(){
        localStorage.setItem(IsGuestKey, JSON.stringify(false));
        localStorage.removeItem(GuestTokenKey);
    }

    SetIsGuest(isGuest: boolean) {
        localStorage.setItem(IsGuestKey, JSON.stringify(isGuest));

        // We want to keep the same guest token between login/sign off attempts.
        // This lets someone sign in an existing account without clearing the
        // guest data
        if (isGuest && localStorage.getItem(GuestTokenKey) === null) {
            localStorage.setItem(GuestTokenKey, crypto.randomUUID().replace("-", ""))
        }
    }

    IsGuest() {
        const value = localStorage.getItem(IsGuestKey);
        return value != null && JSON.parse(value) === true;
    }

    IsGuestOrUser() {
        return this.IsGuest() || this.isLoggedIn;
    }

    Notify() {
        AppLoginStatus.listenerers.forEach(callback => {
            callback(this)
        });
    }
}

const AppLoginStatus = new LoginStatus()

async function SignInGuest() {
    if (AppLoginStatus.IsGuest() || AppLoginStatus.isLoggedIn) {
        console.warn("Attempting guest sign in when already signed in! No action taken.");
        return;
    }

    AppLoginStatus.SetIsGuest(true);
    AppLoginStatus.isLoggedIn = true;
    AppLoginStatus.Notify();
}

async function UpdateSignInStatus() {
    if (AppLoginStatus.IsGuest()) {
        AppLoginStatus.Notify();
        return;
    }

    const response: IUserInfoResponse = await (await fetch(get_current_user)).json();

    AppLoginStatus.isLoggedIn = response.isLoggedIn;
    AppLoginStatus.userId = response.isLoggedIn ? response.userId : "";

    AppLoginStatus.Notify();
    console.log(response);
}

async function SignOut() {
    AppLoginStatus.SetIsGuest(false);
    await fetch(sign_out_user)
    await UpdateSignInStatus();
}

async function SignIn(username: string, password: string) {
    const response : IUserInfoResponse = await (await fetch(sign_in_user, {
        method: "POST",
        headers: {
            Accept: "application/json",
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            username: username,
            password: password,
        }),
    })).json();
    AppLoginStatus.SetIsGuest(false);
    await UpdateSignInStatus();
    return response;
}

async function SignUp(username: string, password: string) {
    const response : IUserInfoResponse = await (await fetch(sign_up_user, {
        method: "POST",
        headers: {
            Accept: "application/json",
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            username: username,
            password: password,
        }),
    })).json();
    await UpdateSignInStatus();
    return response;
}

export default {
    UpdateSignInStatus, SignIn, SignOut, SignUp, SignInGuest, AppLoginStatus
}