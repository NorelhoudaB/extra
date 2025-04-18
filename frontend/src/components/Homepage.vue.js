import { ref } from 'vue';
import { useRouter } from 'vue-router';
const router = useRouter();
const options = ref({
    "/reduire": { title: "Réduire la taille du fichier", description: "Optimisez et compressez votre fichier pour réduire sa taille tout en maintenant la qualité." },
    "/fix-alt": { title: "Corriger Alt dans les images", description: "Corrigez les balises alt manquantes dans les images. Erreur: '{http://www.w3.org/1999/xhtml}img' : L'attribut 'alt' est requis mais manquant." },
    "/convert-xhtml": { title: "Convertir XHTML en HTML", description: "Convertissez votre fichier XHTML en HTML standard." },
    "/fix-table": { title: "Fixer les balises table", description: "Corrigez les erreurs de structure dans les tableaux. Erreur: '{http://www.w3.org/1999/xhtml}table' : Élément(s) enfant manquant(s)." },
    "/fix-space": { title: "Changer les espaces", description: "Remplacez les caractères spéciaux par des espaces classiques dans le code HTML." },
    "/merge-files": { title: "Fusionner les fichiers", description: "Fusionnez jusqu'à trois fichiers HTML/XHTML en un seul fichier." }
});
const navigateTo = (path) => {
    router.push(path);
};
debugger; /* PartiallyEnd: #3632/scriptSetup.vue */
const __VLS_ctx = {};
let __VLS_components;
let __VLS_directives;
// CSS variable injection 
// CSS variable injection end 
__VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
    ...{ class: "container text-center" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.h1, __VLS_intrinsicElements.h1)({
    ...{ class: "display-4 mt-4" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.p, __VLS_intrinsicElements.p)({
    ...{ class: "lead" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.p, __VLS_intrinsicElements.p)({});
__VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
    ...{ class: "row justify-content-center mt-4" },
});
for (const [option, path] of __VLS_getVForSourceType((__VLS_ctx.options))) {
    __VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
        key: (path),
        ...{ class: "col-md-4 mb-4" },
    });
    __VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
        ...{ onClick: (...[$event]) => {
                __VLS_ctx.navigateTo(path);
            } },
        ...{ class: "card option-card text-center" },
    });
    __VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
        ...{ class: "card-body" },
    });
    __VLS_asFunctionalElement(__VLS_intrinsicElements.h5, __VLS_intrinsicElements.h5)({
        ...{ class: "card-title" },
    });
    (option.title);
    __VLS_asFunctionalElement(__VLS_intrinsicElements.p, __VLS_intrinsicElements.p)({
        ...{ class: "card-text" },
    });
    (option.description);
}
/** @type {__VLS_StyleScopedClasses['container']} */ ;
/** @type {__VLS_StyleScopedClasses['text-center']} */ ;
/** @type {__VLS_StyleScopedClasses['display-4']} */ ;
/** @type {__VLS_StyleScopedClasses['mt-4']} */ ;
/** @type {__VLS_StyleScopedClasses['lead']} */ ;
/** @type {__VLS_StyleScopedClasses['row']} */ ;
/** @type {__VLS_StyleScopedClasses['justify-content-center']} */ ;
/** @type {__VLS_StyleScopedClasses['mt-4']} */ ;
/** @type {__VLS_StyleScopedClasses['col-md-4']} */ ;
/** @type {__VLS_StyleScopedClasses['mb-4']} */ ;
/** @type {__VLS_StyleScopedClasses['card']} */ ;
/** @type {__VLS_StyleScopedClasses['option-card']} */ ;
/** @type {__VLS_StyleScopedClasses['text-center']} */ ;
/** @type {__VLS_StyleScopedClasses['card-body']} */ ;
/** @type {__VLS_StyleScopedClasses['card-title']} */ ;
/** @type {__VLS_StyleScopedClasses['card-text']} */ ;
var __VLS_dollars;
const __VLS_self = (await import('vue')).defineComponent({
    setup() {
        return {
            options: options,
            navigateTo: navigateTo,
        };
    },
});
export default (await import('vue')).defineComponent({
    setup() {
        return {};
    },
});
; /* PartiallyEnd: #4569/main.vue */
