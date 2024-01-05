<script lang="ts">
    import { onMount } from 'svelte'; 
    
    export let title: string;

</script>

<column class="rounded_border">
    <slot/>
    <h1>{title}</h1>
</column>
<style>
    h1{
        font-size: 1rem;
        margin: 0;
        margin-top: 10px;
    }

    column{
        row-gap: 0;
        padding: 10px;
        width: 80px;
        height: 80px;
        cursor: pointer;
    }

    column:hover{
        border-bottom: 5px solid #13132f;
        border-left: 2px solid #13132f;
        border-right: 2px solid #13132f;
        border-top: 1px solid #13132f;
    }
</style>