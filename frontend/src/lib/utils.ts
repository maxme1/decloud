import type { Element } from "./client";

export function* elementWalker(x: Element): Iterable<Element> {
    yield x;

    if ('elements' in x && x.elements && (x.elements[0] instanceof Element)) {
        for (const child of x.elements) {
            yield* elementWalker(child);
        }
    }
    if ('element' in x && x.element && (x.element instanceof Element)) {
        yield* elementWalker(x.element);
    }
    if ('text' in x && x.text && (x.text instanceof Element)) {
        yield* elementWalker(x.text as Element);
    }
}
