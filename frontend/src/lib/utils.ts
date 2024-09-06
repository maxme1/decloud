import type { Element } from "./client";

export function* elementWalker(x: Element): Iterable<Element> {
    if (!x || typeof x !== 'object') return;

    yield x;

    if ('elements' in x && x.elements) {
        for (const child of x.elements) {
            yield* elementWalker(child);
        }
    }
    if ('element' in x && x.element) {
        yield* elementWalker(x.element);
    }
    if ('text' in x && x.text) {
        yield* elementWalker(x.text as Element);
    }
}
