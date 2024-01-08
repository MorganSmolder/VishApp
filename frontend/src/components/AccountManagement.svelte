<script>
    import LogOutButton from "./LogOutButton.svelte";
    import Login from "../login";
</script>

<!-- we are just stopping clicks here, don't need to worry about ally -->
<!-- svelte-ignore a11y-click-events-have-key-events -->
<!-- svelte-ignore a11y-no-static-element-interactions -->
<anchor on:click={(e => e.stopPropagation())}>
    <column class="parent rounded_border"> 
        <h2>Logged in as {Login.AppLoginStatus.userId}</h2>
        <LogOutButton></LogOutButton>
    </column>
</anchor>
<style>

    h2{
        font-size: 18px;
    }

    column{
        padding:10px;
        min-width: 200px;
        row-gap: 0;
    }
</style>