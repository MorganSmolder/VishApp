import Login from "./login";

const backend_endpoint: string = `/api`;
const sync_chunk: string = `${backend_endpoint}/syncChunk`;
const get_entry: string = `${backend_endpoint}/getEntry`;
const get_entries_for_month: string = `${backend_endpoint}/getEntriesForMonth`;
const get_streak: string = `${backend_endpoint}/getStreak`

const IndexKey = "Index";

interface IJournalEntry {
    key: string;
    textContent: string;
    modifiedTime: number;
    lastSyncTime: number;
}

interface IServerJournalEntry {
    textContent: string;
    modifiedTime: number;
}

interface IGetEntryResponse {
    entry: IServerJournalEntry | null;
}

interface IGetEntriesForMonthResponse {
    entries: number[] | null;
}

interface IGetStreakResponse {
    streak: number;
}

class DataStore {
    loadedEntries: { [key: string]: IJournalEntry; }

    constructor() {
        this.loadedEntries = {}
    }

    private GetKey(date: Date) {
        const id = Login.AppLoginStatus.GetIdentifier();
        const year = date.getFullYear();
        const month = date.getMonth() + 1;
        const day = date.getDate();
        return `${id}-${year}-${month}-${day}`;
    }

    public async MarkEntrySynced(key: string) {
        delete this.loadedEntries[key];
        localStorage.removeItem(key);
        this.RemoveKeyFromIndex(key);
    }

    public async UpdateEntry(date: Date, newContent: string) {
        const key = this.GetKey(date);
        const entry = await this.AccessEntryRaw(key);
        entry.textContent = newContent;
        entry.modifiedTime = new Date().getTime();

        this.loadedEntries[key] = entry;
        localStorage.setItem(key, JSON.stringify(entry));

        this.AddKeyToIndex(key)
    }

    public async AccessEntry(date: Date) {
        const key = this.GetKey(date);

        // if we are logged in, see if the server has an entry
        if (Login.AppLoginStatus.isLoggedIn) {
            let response: IGetEntryResponse = await (await fetch(get_entry, {
                method: "POST",
                headers: {
                    Accept: "application/json",
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ "key": key }),
            })).json();

            // add the entry to local storage so we can edit it
            if (response.entry != null) {
                var entry = response.entry;
                var newEntry: IJournalEntry = {
                    key: key,
                    textContent: entry.textContent,
                    lastSyncTime: entry.modifiedTime,
                    modifiedTime: entry.modifiedTime,
                };
                this.loadedEntries[key] = newEntry;
                this.AddKeyToIndex(key);
                localStorage.setItem(key, JSON.stringify(newEntry));
            }
        }

        return (await this.AccessEntryRaw(key));
    }

    public SetIndex(index: string[]) {
        localStorage.setItem(IndexKey, JSON.stringify(index));
    }

    public AccessIndex() {
        const json = localStorage.getItem(IndexKey);
        const index: string[] = json === null
            ? []
            : JSON.parse(json);
        return index;
    }

    private AddKeyToIndex(key: string) {
        const index = this.AccessIndex();
        if (index.indexOf(key) === -1) {
            index.push(key);
            localStorage.setItem(IndexKey, JSON.stringify(index));
        }
    }

    private RemoveKeyFromIndex(key: string) {
        let index = this.AccessIndex();
        const idx = index.indexOf(key);
        index = index.splice(idx, 1);
        this.SetIndex(index);
    }

    public async AccessEntryRaw(key: string) {
        if (key in this.loadedEntries) {
            return this.loadedEntries[key];
        }

        const json = localStorage.getItem(key);

        const entry: IJournalEntry = json !== null
            ? JSON.parse(json)
            : {
                textContent: "",
                modifiedTime: new Date().getTime(),
                lastSyncTime: 0,
                key: key
            };

        this.loadedEntries[key] = entry;
        return entry;
    }

    private MonthDays(date: Date) {
        var d = new Date(date.getFullYear(), date.getMonth() + 1, 0);
        return d.getDate();
    }

    public async GetEntriesForMonth(year: number, month: number) {
        var date = new Date(year, month);
        const days = this.MonthDays(date);

        if (Login.AppLoginStatus.isLoggedIn) {
            let response: IGetEntriesForMonthResponse = await (await fetch(get_entries_for_month, {
                method: "POST",
                headers: {
                    Accept: "application/json",
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ "year": year, "month": month }),
            })).json();

            if (response.entries !== null) {
                const entries = []
                for (var day = 1; day <= days; day++) {
                    const entryExists = response.entries.indexOf(day) !== -1;
                    entries.push(entryExists)
                }

                return entries;
            }
        }

        const entries = []
        for (var day = 1; day <= days; day++) {
            const key = this.GetKey(new Date(year, month, day));
            const entryExists = key in localStorage;
            entries.push(entryExists)
        }

        return entries;
    }

    public async GetStreak(today: Date) {
        if (Login.AppLoginStatus.isLoggedIn) {
            let response: IGetStreakResponse = await (await fetch(get_streak, {
                method: "POST",
                headers: {
                    Accept: "application/json",
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ "key": this.GetKey(today) }),
            })).json();

            return response.streak;
        }
        
        let streak = 0;
        let index = this.AccessIndex();
        if (index.length == 0){
            return streak;
        }

        let dates = [];

        for (let key of index)
        {
            if(this.ParseId(key) != Login.AppLoginStatus.GetGuestKey())
            {
                continue;
            }
            dates.push(this.ParseKey(key))
        }

        dates.sort((a,b)=>a.getTime()-b.getTime());

        const lastEntry = dates[dates.length - 1];
        let walk = today;

        if(!this.CompareDates(walk, lastEntry)){
            walk = this.DayBefore(walk);
            if(!this.CompareDates(walk, lastEntry))
            {
                return streak;
            }
        }

        for(var i = dates.length - 1; i >= 0; i--)
        {
            const entryDate = dates[i];
            if(!this.CompareDates(entryDate, walk)){
                return streak;
            }
            walk = this.DayBefore(walk);
            streak++;
        }

        return streak;
    }

    private DayBefore(day : Date){
        var dayBefore = new Date(day.getTime());
        dayBefore.setDate(day.getDate() - 1);
        return dayBefore;
    }

    private ParseKey(key : string)
    {
        const parts = key.split("-");
        const year = parseInt(parts[1]);
        const month = parseInt(parts[2]) - 1;
        const day = parseInt(parts[3]);

        return new Date(year, month, day);
    }

    public ParseId(key : string)
    {
        return key.split("-")[0];
    }

    private CompareDates(a : Date, b : Date)
    {
        const yearA = a.getFullYear();
        const monthA = a.getMonth() + 1;
        const dayA = a.getDate();

        const yearB = b.getFullYear();
        const monthB = b.getMonth() + 1;
        const dayB = b.getDate();

        return yearA == yearB && monthA == monthB && dayA == dayB; 
    }
}

const GlobalDataStore = new DataStore();

async function ConvertGuestToUser(username: string, password: string) {
    console.assert(Login.AppLoginStatus.IsGuest());
    // attempt to create the new user
    const response = await Login.SignUp(username, password);

    if (response.isLoggedIn) {
        // rewrite local storage to associate journal entries with the new user
        // sync loop will then automatically push the stored data to the server
        const index = GlobalDataStore.AccessIndex();
        const newIndex = [];
        for (const oldKey of index) {
            const keyParts = oldKey.split('-');
            keyParts[0] = response.userId;
            const newKey = keyParts.join('-');

            const value = localStorage.getItem(oldKey);
            if (value == null) {
                console.warn("Null journal entry found. This should not happen.")
                continue;
            }
            localStorage.removeItem(oldKey);
            localStorage.setItem(newKey, value);
            newIndex.push(newKey)
        }
        GlobalDataStore.SetIndex(newIndex);

        // We no longer need to keep the guest token
        Login.AppLoginStatus.DestroyGuest();
    }
}

interface ICommitResult {
    success: Boolean;
}

async function SyncData() {
    if (!Login.AppLoginStatus.isLoggedIn) {
        return;
    }

    const toSync: IJournalEntry[] = [];

    // Grab the items that need to be synced
    for (const key of GlobalDataStore.AccessIndex()) {
        const entry = await GlobalDataStore.AccessEntryRaw(key);
        const needsSync = entry.lastSyncTime < entry.modifiedTime;

        const id = GlobalDataStore.ParseId(key);

        // we don't sync guest entries
        if(id == Login.AppLoginStatus.GetGuestKey())
        {
            continue;
        }

        if (needsSync) {
            toSync.push(entry);
        }
    }

    // attempt the sync
    if (toSync.length !== 0) {
        (await fetch(sync_chunk, {
            method: "POST",
            headers: {
                Accept: "application/json",
                "Content-Type": "application/json",
            },
            body: JSON.stringify(toSync),
        })).json().then(async json => {
            const data: ICommitResult = json;
            if (data.success) {
                // we can remove the item if it was synced
                for (let i of toSync) {
                    console.log(`UPDATED: ${i.key}`)
                    GlobalDataStore.MarkEntrySynced(i.key);
                }
            }
        });
    }
}

function StartTickingSync() {
    setInterval(() => {
        SyncData()
    }, 300);
}

export default {
    GlobalDataStore, SyncData, StartTickingSync, ConvertGuestToUser
}