<script lang="ts">
    import Login from "../login";
    import { goto } from '$app/navigation';

    let isLoggedIn = false;

    Login.AppLoginStatus.listenerers.push((status) => {
        isLoggedIn = status.IsGuestOrUser();
    });
</script>

<button
    on:click={async () => {
        await Login.SignOut();
        goto("/");
    }}>Sign Out</button
>
