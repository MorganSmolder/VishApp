<script lang="ts">
    export let description: string;
    export let tag: string;
    export let image: string;
</script>

<div class=" card">
    <column style="align-items:center">
        <img
            src={image}
            alt="Avatar"
            style="width:200px;height:200px;"
        />
        <h2>{tag}</h2>
    </column>
</div>

<style>
    @import "./shared.css";

    .card {
        width: 250PX;
        height: 250PX;
        overflow: hidden;
        text-align: center;
    }
</style>
