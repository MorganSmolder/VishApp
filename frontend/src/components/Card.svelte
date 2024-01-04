<script lang="ts">
</script>

<div class=" card">
    <column style="align-items:center">
        <slot/>
    </column>
</div>

<style>
    column{
        row-gap: 0;
    }
    .card {
        overflow: hidden;
        text-align: center;
        flex:1;
    }

</style>
