
interface TextLike {
    type:
    | "plain"
    | "hashtag"
    | "link"
    | "code"
    | "email"
    | "phone"
    | "mention"
    | "bold"
    | "italic";
    text: string;
}
interface Pre {
    type: "pre";
    text: string;
    language: string;
}
interface TextLink {
    type: "text_link";
    text: string;
    href: string;
}
interface Location {
    latitude: number;
    longitude: number;
}
interface Contact {
    phone_number: string;
    first_name: string;
    last_name: string;
}

interface Message {
    type: "message" | "service";
    from: string;
    text: string | undefined;
    text_entities: (TextLike | Pre | TextLink)[];
    date: string;
    date_unixtime: number;
    // modifiers
    edited: string | undefined;
    reply_to_message_id: number | undefined;
    forwarded_from: string | undefined;
    via_bot: string | undefined;
    // actions
    action: "phone_call" | undefined;
    actor: string | undefined;
    discard_reason: string | undefined;
    // media
    media_type:
    | "sticker"
    | "animation"
    | "video_file"
    | "audio_file"
    | "voice_message"
    | "video_message"
    | undefined;
    photo: string | undefined;
    file: string | undefined;
    thumbnail: string | undefined;
    mime_type: string | undefined;
    location_information: Location | undefined;
    contact_information: Contact | undefined;
    live_location_period_seconds: number | undefined;
}

function groupMessages(messages: Message[]): Message[][] {
    let result: Message[][] = [];
    let current: Message[] = [];
    for (let i = 0; i < messages.length; i++) {
        const message = messages[i];
        if (current.length === 0 || !(message.type === "service" || message.from !== current[0].from)) {
            current.push(message);
        } else {
            result.push(current);
            current = [message];
        }
    }
    if (current.length > 0) {
        result.push(current);
    }
    return result
}

export { type Message, groupMessages };