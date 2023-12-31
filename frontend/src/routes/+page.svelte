<script>
    import Hero from "./Hero.svelte";
    import Card from "./Card.svelte";

    import Notebook from "$lib/images/notebook.png";
    import Live from "$lib/images/live.png";
    import Brain from "$lib/images/brain.png";
    import Loop from "$lib/images/loop.png";
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
</container>
<style>
	@import './shared.css';

    h2{
        text-align: center;
        font-size: 32px;
    }
</style>
