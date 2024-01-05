<script lang="ts">
	import { fade } from 'svelte/transition';
	import { scale } from 'svelte/transition';
	import { quintOut } from 'svelte/easing';

    export let isVisible : Boolean = false;
</script>

{#if isVisible}
<modal_parent transition:fade={{ delay: 0, duration: 300 }}>
    <column transition:scale={{ duration: 300, delay: 0, opacity: 0.5, start: 0.5, easing: quintOut }}>
        <modal>
            <slot />
        </modal>
    </column>
</modal_parent>
{/if}
<style>
    modal_parent {
        position: fixed;
        z-index: 1;
        display: block;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.5);
        top: 0;
        left: 0;
    }

    modal {
        border-radius: 15px;
        background-color: white;
        display: block;
        width: 400px;
        height: 300px;
        overflow: hidden;
    }

    column {
        height: 100%;
        text-align: center;
    }
</style>
