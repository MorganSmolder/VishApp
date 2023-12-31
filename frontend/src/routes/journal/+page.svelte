<script lang="ts">
    import { onMount } from "svelte";

    const backend_endpoint = "http://127.0.0.1:5000/tst";

    let prevPost : HTMLButtonElement;
    let nextPost : HTMLButtonElement;

    onMount(async () => {
        var options = {
            method: "GET", // *GET, POST, PUT, DELETE, etc.
            mode: "no-cors", // no-cors, *cors, same-origin
            cache: "no-cache", // *default, no-cache, reload, force-cache, only-if-cached
            credentials: "same-origin", // include, *same-origin, omit
            headers: {
            "Content-Type": "application/json",
            // 'Content-Type': 'application/x-www-form-urlencoded',
            },
            redirect: "follow", // manual, *follow, error
            referrerPolicy: "no-referrer", // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
        };
        const data = await fetch(backend_endpoint, {
            method: "GET", // *GET, POST, PUT, DELETE, etc.
            mode: "no-cors", // no-cors, *cors, same-origin
            cache: "no-cache", // *default, no-cache, reload, force-cache, only-if-cached
            credentials: "same-origin", // include, *same-origin, omit
            headers: {
            "Content-Type": "application/json",
            // 'Content-Type': 'application/x-www-form-urlencoded',
            },
            redirect: "follow", // manual, *follow, error
            referrerPolicy: "no-referrer", // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
        });
        console.log(data);
    });
</script>

<container>
    <column>
        <h1>test</h1>
        <expand_row>
            <button bind:this={prevPost} >&lt;</button>
            <input type="date" value="2017-06-01" />
            <button bind:this={nextPost} >&gt;</button>
        </expand_row>
        <textarea> </textarea>
    </column>
</container>

<style>
    @import "../shared.css";

    textarea {
        margin: 2rem;
        width: 100%;
        min-height: 500px;
        border: none;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        padding: 25px;
        border-radius: 25px;
        resize: none;
        font-size: 32px;
    }

    textarea:focus-visible {
        border: none;
        outline: none;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
    }
</style>
