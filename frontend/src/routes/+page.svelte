<script lang="ts">
    import { onMount } from "svelte";

    import Hero from "../components/Hero.svelte";
    import Card from "../components/Card.svelte";
    import Modal from "../components/Modal.svelte";

    import Notebook from "$lib/images/notebook.png";
    import Live from "$lib/images/live.png";
    import Brain from "$lib/images/brain.png";
    import Loop from "$lib/images/loop.png";

    var viewSignUp: Boolean = true;
    var needsSignIn: Boolean = false;

    var usernameInput: HTMLInputElement;
    var passwordInput: HTMLInputElement;

    const backend_endpoint: string = `/api`;
    const get_current_user: string = `${backend_endpoint}/getUser`;
    const sign_in_user: string = `${backend_endpoint}/signIn`;
    const sign_out_user: string = `${backend_endpoint}/signOut`;
    const sign_up_user: string = `${backend_endpoint}/signUp`;

    async function UpdateSignInStatus() {
        return await (await fetch(get_current_user)).json().then((json) => {
            needsSignIn = !json.isLoggedIn;
        });
    }

    async function SignOut() {
        await fetch(sign_out_user);
        needsSignIn = true;
    }

    async function SignIn() {
        return await fetch(sign_in_user, {
            method: "POST",
            headers: {
                Accept: "application/json",
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                username: usernameInput.value,
                password: passwordInput.value,
            }),
        }).then((json) => {
            UpdateSignInStatus();
        });
    }

    async function SignUp() {
        return await fetch(sign_up_user, {
            method: "POST",
            headers: {
                Accept: "application/json",
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                username: usernameInput.value,
                password: passwordInput.value,
            }),
        }).then((json) => {
            console.log(json)
            UpdateSignInStatus();
        });
    }


    function TabExisting() {
        viewSignUp = false;
    }

    function TabNew() {
        viewSignUp = true;
    }

    onMount(async () => {
        await UpdateSignInStatus();
    });
</script>

<Hero></Hero>
<container>
    <row style="width:1200px; margin:2rem auto;">
        <Card description="hi" image={Live} tag="Live"></Card>
        <Card description="hi" image={Notebook} tag="Journal"></Card>
        <Card description="hi" image={Brain} tag="Reflect"></Card>
        <Card description="hi" image={Loop} tag="Repeat"></Card>
    </row>
    <h2 style="margin:3rem;">We'll handle the technical stuff</h2>
    {#if !needsSignIn}
        <button on:click={SignOut}>Sign Out</button>
    {/if}
</container>
<Modal isVisible={needsSignIn}>
    <row>
        <button on:click={TabNew}>New User</button>
        <button on:click={TabExisting}>Existing User</button>
    </row>
    {#if viewSignUp}
        <column>
            <h1>Sign Up</h1>
            <input bind:this={usernameInput} type="text" />
            <input bind:this={passwordInput} type="text" />
            <button on:click={SignUp}>Sign In</button>
        </column>
    {:else}
        <column>
            <h1>Sign In</h1>
            <input bind:this={usernameInput} type="text" />
            <input bind:this={passwordInput} type="text" />
            <button on:click={SignIn}>Sign In</button>
        </column>
    {/if}
</Modal>

<style>
    @import "../shared.css";

    h2 {
        text-align: center;
        font-size: 32px;
    }

    button:hover {
        background-color: #ff3f8f;
    }
</style>
