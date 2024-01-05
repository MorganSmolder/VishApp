<script lang="ts">
    import Hero from "../components/Hero.svelte";
    import Card from "../components/Card.svelte";

    import SignInForm from "../components/SignInForm.svelte";
    import LogOutButton from "../components/LogOutButton.svelte";
    import Arrow from "../components/Arrow.svelte";
</script>
<Hero></Hero>
<container>
    <row class="" style="width:auto; margin:2rem; ">
        <Card> 
            <lord-icon
                src="https://cdn.lordicon.com/dnojsmko.json"
                trigger="hover">
            </lord-icon>
            <h3>Live</h3>
            <p>Just do your normal everyday thing</p>
        </Card>
        <Arrow></Arrow>
        <Card>
            <lord-icon
                src="https://cdn.lordicon.com/gwlusjdu.json"
                trigger="hover">
            </lord-icon>
            <h3>Journal</h3>
            <p>Log in every day to write a journal entry</p>
        </Card>
        <Arrow></Arrow>
        <Card>
            <lord-icon
                src="https://cdn.lordicon.com/wznuqbba.json"
                trigger="hover">
            </lord-icon>
            <h3>Reflect</h3>
            <p>Read past entries to reflect on your journey</p>
        </Card>
        <Arrow></Arrow>
        <Card>
            <lord-icon
                src="https://cdn.lordicon.com/gnjkudty.json"
                trigger="hover" >
            </lord-icon>
            <h3>Repeat</h3>
            <p>Keep the streak going as long as you can</p>
        
        </Card>
    </row>
    <h2 style="margin:3rem;">Build a better you one day at a time!</h2>
    
</container>
<SignInForm></SignInForm>
<style>
    h2 {
        text-align: center;
        font-size: 32px;
    }

    lord-icon{
        width: 100px;
        height: 100px;
    }

    @media only screen and (max-width: 1000px) {
        .rounded_border{
            border: none;
        }

        lord-icon{
            width: 200px;
            height: 200px;
        }
    }
</style>
