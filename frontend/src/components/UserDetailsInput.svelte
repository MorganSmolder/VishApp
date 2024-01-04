<script lang="ts">
    import { createEventDispatcher } from "svelte";
    const dispatch = createEventDispatcher();
    
    export let serverError = "";
    
    function NotifySubmit() {
        ValidateUsername();
        ValidatePassword();
        showUsernameError = true;
        showPasswordError = true;

        if (!usernameValid || !passwordValid) {
            return;
        }
    
        dispatch("submit", {
            username: usernameInput.value,
            password: passwordInput.value,
        });
    }

    let usernameInput: HTMLInputElement;
    let passwordInput: HTMLInputElement;

    let usernameValid = false;
    let passwordValid = false;
    let showUsernameError = false;
    let showPasswordError = false;


    function ValidateUsername() {
        usernameValid = ValidateEmail(usernameInput.value);
    }

    function ValidatePassword() {
        passwordValid = passwordInput.value.length >= 8;
    }

    function ValidateEmail(email: string) {
        return (
            String(email)
                .toLowerCase()
                .match(
                    /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|.(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/,
                ) != null
        );
    }
</script>

<form on:submit={NotifySubmit}>
    <column>
        <label for="username">Email</label>
        <input
            id="username"
            bind:this={usernameInput}
            type="email"
            on:input={ValidateUsername}
            on:blur={() => (showUsernameError = true)}
        />
        <error style="opacity: {showUsernameError && !usernameValid ? 1 : 0};">Invalid Email!</error>
        <label for="password">Password</label>
        <input
            id="password"
            bind:this={passwordInput}
            type="password"
            on:input={ValidatePassword}
            on:blur={() => (showPasswordError = true)}
        />
        <error style="opacity: {showPasswordError && !passwordValid ? 1 : 0};">Invalid Password! Must be at least 8 characters.</error>
        <input type="submit" />
        <error style="opacity: {serverError != "" ? 1 : 0};">{serverError}</error>
    </column>
</form>

<style>
    error {
        color: red;
        font-weight: bold;
        font-size: 14px;
    }

    column{
        row-gap: 10px;
    }
</style>
