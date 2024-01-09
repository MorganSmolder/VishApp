<script lang="ts">
    import Login from "../login";
    import { goto } from '$app/navigation';  
    import { browser } from '$app/environment';
 

    let isLoggedIn = false;

    Login.AppLoginStatus.listenerers.push((status) => {
        isLoggedIn = status.IsGuestOrUser();
    });
</script>

<button
    on:click={async () => {
        await Login.SignOut();
                
        if (browser) {
            window.location.href = "/"
        }
    }}>Sign Out</button
>
