<script lang="ts">
    import { onMount } from "svelte";
    import { createEventDispatcher } from "svelte";

    
    import Modal from "../components/Modal.svelte";
    import TabView from "../components/TabView.svelte";
    
    import Login from "../login";
    import UserDetailsInput from "./UserDetailsInput.svelte";
    
    export let active : boolean;

    const dispatch = createEventDispatcher();

    function NotifyComplete() {
        dispatch("complete", {
            loggedIn : Login.AppLoginStatus.IsGuestOrUser(),
        });
    }

    let isLoggedIn = true;

    let errorSignIn = "";
    let errorSignUp = "";

    Login.AppLoginStatus.listenerers.push((status) => {
        isLoggedIn = status.IsGuestOrUser();
    });

    onMount(async () => {
        Login.UpdateSignInStatus();
    });

    async function SignIn(evt){
        const username = evt.detail.username;
        const password = evt.detail.password;
        const response = await Login.SignIn(username, password);
        errorSignIn = response.message;
        NotifyComplete();
    }

    async function SignUp(evt){
        const username = evt.detail.username;
        const password = evt.detail.password;
        const response = await Login.SignUp(username, password);
        errorSignUp = response.message;
        NotifyComplete();
    }

    function ClearErrorMessages(){
        errorSignIn = "";
        errorSignUp = "";
    }
</script>

<Modal isVisible={!isLoggedIn && active}>
    <TabView on:tabchange={ClearErrorMessages} headerB="Sign In" headerC="Sign Up" headerA="Guest">
        <padded_div slot="body_a">
            <column>
                <p>If you create a guest account your journal entries will only be available on this computer. You can upgrade to a full account at any time.</p>
                <button style="margin:20px"
                    on:click={async () => {
                        await Login.SignInGuest();
                        NotifyComplete();
                    }}>Continue As Guest</button
                >
            </column>
        </padded_div>
        <padded_div slot="body_b">
            <UserDetailsInput serverError={errorSignIn} on:submit={SignIn}></UserDetailsInput>
        </padded_div>
        <padded_div slot="body_c">
            <UserDetailsInput serverError={errorSignUp} on:submit={SignUp}></UserDetailsInput>
        </padded_div>
    </TabView>
    
</Modal>

<style>
    padded_div {
        display: block;
        padding: 20px;
    }

    error {
        color: red;
        font-weight: bold;
    }
</style>
