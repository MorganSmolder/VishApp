class QuerySettings {
    useLocalStorage: boolean;

    constructor(useLocalStorage: boolean) {
        this.useLocalStorage = useLocalStorage;
    }
}

interface IJournalEntries {
    lastEntry: Date | null;
    data: { [day: number]: IJournalEntry; };
}

interface IJournalEntry {
    textContent: string | null;
}


const Settings = new QuerySettings(true);

function GetKey(year: number, month: number) {
    return `${year}-${month}`;
}

function GetJournalEntries(year: number, month: number): IJournalEntries {
    if (!Settings.useLocalStorage) {
        return { lastEntry:null, data: {} };
    }

    var key = GetKey(year, month);
    var data = localStorage.getItem(key);

    if (!data) {
        return { lastEntry:null, data: {} };
    }

    return JSON.parse(data);
}

function WriteJournalEntries(year: number, month: number, journalEntries: IJournalEntries) {
    if (!Settings.useLocalStorage) {
        return;
    }

    var data = JSON.stringify(journalEntries);
    var key = GetKey(year, month);

    localStorage.setItem(key, data);
}

export type{IJournalEntries};
export default {
    WriteJournalEntries, GetJournalEntries, Settings
}