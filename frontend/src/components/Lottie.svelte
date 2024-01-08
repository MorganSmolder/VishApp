<script lang="ts">
    import { onMount } from "svelte";

    export let src: string;

    export let playOnEnter = true;
    let player: any;

    function PlayAnim() {
            if (!playOnEnter || player.playerInstance == undefined) {
            return;
        }

        if (player.playerInstance.isPlaying) {
            return;
        }

        player.playerInstance.playFromBeginning();

        // const isPlaying = player.getState().currentState == "playing";
        // if (isPlaying) {
        //     return;
        // }
        // player.stop();
        // player.play();
    }

    onMount(() => {
        player.src = src;
    });
</script>

<lord-icon
    bind:this={player}
    on:mouseenter={PlayAnim}
    {src}
    style="width:250px;height:250px"
    loading="lazy"
>
</lord-icon>
<!-- <dotlottie-player
    bind:this={player}
    on:mouseenter={PlayAnim}
    background="transparent"
    speed="1"
    style="width: 300px; height: 300px"
    autoplay
>
</dotlottie-player>
<lord-icon bind:this={player}>

</lord-icon> -->
