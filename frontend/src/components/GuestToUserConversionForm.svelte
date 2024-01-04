<script lang="ts">
    import Login from "../login";
    let isLoggedIn = false;
    Login.AppLoginStatus.listenerers.push(status => {
        isLoggedIn = status.isLoggedIn;
    });
</script>
{#if !isLoggedIn}
<row>
    <p>You are currently using MindSpace as a guest. Create an account to save your progress across devices.</p>
    <column style="flex:.5">
        <input type="text" />
        <input type="text" />
        <button>Sign Up</button>
    </column>
</row>
{/if}
<style>
    column{
        row-gap: 0;
    }
    
    p{
        font-size: 1.5em;
        flex: 1;
    }
</style>