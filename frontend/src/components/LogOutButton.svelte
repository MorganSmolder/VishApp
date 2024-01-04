<script lang="ts">
    import Login from "../login";

    let isLoggedIn = false;

    Login.AppLoginStatus.listenerers.push((status) => {
        isLoggedIn = status.IsGuestOrUser();
    });
</script>
{#if isLoggedIn}
    <button on:click={() => Login.SignOut()}>Sign Out</button>
{/if}