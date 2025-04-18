import { ref, computed } from 'vue';
import { useRoute } from 'vue-router';
const props = defineProps({
    description: String
});
const isLoading = ref(false);
const selectedFile = ref(null);
const selectedFiles = ref([null, null, null]); // For merge-files route
const fileError = ref("");
const route = useRoute();
const cancelUpload = () => {
    isLoading.value = false;
    if (route.path === '/merge-files') {
        selectedFiles.value = [null, null, null];
    }
    else {
        selectedFile.value = null;
    }
    fileError.value = "";
    // Reset all input fields
    if (route.path === '/merge-files') {
        for (let i = 0; i < 3; i++) {
            const fileInput = document.getElementById(`file-upload-${i}`);
            if (fileInput)
                fileInput.value = "";
        }
    }
    else {
        const fileInput = document.getElementById("file-upload");
        if (fileInput)
            fileInput.value = "";
    }
};
const defaultDescriptions = {
    "/reduire": "Optimisez et compressez votre fichier pour réduire sa taille tout en maintenant la qualité.",
    "/fix-alt": "Corrigez les balises alt manquantes dans les images. Erreur: '{http://www.w3.org/1999/xhtml}img' : The attribute 'alt' is required but missing",
    "/convert-xhtml": "Convertissez votre fichier XHTML en HTML standard.",
    "/fix-table": "Corrigez les erreurs de structure dans les tableaux. Erreur: '{http://www.w3.org/1999/xhtml}table': Missing child element(s)",
    "/fix-space": "Changer les caractères spéciaux par des espaces classique dans le code HTML.",
    "/merge-files": "Fusionnez jusqu'à trois fichiers HTML/XHTML en un seul fichier."
};
const description = computed(() => props.description || defaultDescriptions[route.path] || "Upload a file");
const isValidFileType = (file) => file && /\.(xhtml|html)$/i.test(file.name);
const hasValidFiles = computed(() => {
    if (route.path === '/merge-files') {
        return selectedFiles.value.some(file => file !== null);
    }
    return selectedFile.value !== null;
});
const handleFileChange = (event, index = null) => {
    const file = event.target.files[0];
    if (!file)
        return;
    if (isValidFileType(file)) {
        if (route.path === '/merge-files' && index !== null) {
            selectedFiles.value[index] = file;
        }
        else {
            selectedFile.value = file;
        }
        fileError.value = "";
    }
    else {
        fileError.value = "Seuls les fichiers HTML et XHTML sont autorisés.";
        event.target.value = null;
        if (route.path === '/merge-files' && index !== null) {
            selectedFiles.value[index] = null;
        }
        else {
            selectedFile.value = null;
        }
    }
};
const handleDrop = (event, index = null) => {
    event.preventDefault();
    const file = event.dataTransfer.files[0];
    if (!file)
        return;
    if (isValidFileType(file)) {
        if (route.path === '/merge-files' && index !== null) {
            selectedFiles.value[index] = file;
        }
        else {
            selectedFile.value = file;
        }
        fileError.value = "";
    }
    else {
        fileError.value = "Seuls les fichiers HTML et XHTML sont autorisés.";
        if (route.path === '/merge-files' && index !== null) {
            selectedFiles.value[index] = null;
        }
        else {
            selectedFile.value = null;
        }
    }
};
const removeFile = (index) => {
    selectedFiles.value[index] = null;
    const fileInput = document.getElementById(`file-upload-${index}`);
    if (fileInput)
        fileInput.value = "";
};
const uploadFile = async () => {
    if ((route.path === '/merge-files' && !selectedFiles.value.some(f => f)) ||
        (route.path !== '/merge-files' && !selectedFile.value)) {
        return;
    }
    isLoading.value = true;
    const formData = new FormData();
    if (route.path === '/merge-files') {
        if (selectedFiles.value[0])
            formData.append("file_one", selectedFiles.value[0]);
        if (selectedFiles.value[1])
            formData.append("file_two", selectedFiles.value[1]);
        if (selectedFiles.value[2])
            formData.append("file_three", selectedFiles.value[2]);
    }
    else {
        formData.append("file", selectedFile.value);
    }
    try {
        const response = await fetch(`${import.meta.env.VITE_API_BASE_URL}${route.path}`, {
            method: "POST",
            body: formData
        });
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || "File upload failed");
        }
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        let filename = '';
        if (route.path === '/merge-files') {
            if (selectedFiles.value[1]) {
                filename = selectedFiles.value[1].name;
            }
            else {
                fileError.value = "Le deuxième fichier est requis pour le nom de sortie.";
                return;
            }
        }
        else if (route.path === "/convert-xhtml") {
            if (selectedFile.value) {
                filename = selectedFile.value.name.replace(/\.(xhtml|html)$/i, ".html");
            }
            else {
                fileError.value = "Aucun fichier sélectionné.";
                return;
            }
        }
        else {
            if (selectedFile.value) {
                filename = selectedFile.value.name;
            }
            else {
                fileError.value = "Aucun fichier sélectionné.";
                return;
            }
        }
        const link = document.createElement("a");
        link.href = url;
        link.setAttribute("download", filename);
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }
    catch (error) {
        console.error("File upload failed:", error);
        fileError.value = error.message || "Une erreur s'est produite lors de l'envoi des fichiers";
    }
    finally {
        isLoading.value = false;
    }
};
const allMergeFilesSelected = computed(() => {
    return route.path === '/merge-files' &&
        selectedFiles.value.filter(f => f).length >= 2; //or 3 default 
});
debugger; /* PartiallyEnd: #3632/scriptSetup.vue */
const __VLS_ctx = {};
let __VLS_components;
let __VLS_directives;
/** @type {__VLS_StyleScopedClasses['upload-box']} */ ;
/** @type {__VLS_StyleScopedClasses['annuler']} */ ;
// CSS variable injection 
// CSS variable injection end 
__VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
    ...{ class: "container" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
    ...{ class: "description-box" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.p, __VLS_intrinsicElements.p)({});
(__VLS_ctx.description);
__VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
    ...{ class: "upload-container" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
    ...{ class: "upload-content" },
});
if (__VLS_ctx.route.path !== '/merge-files') {
    __VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
        ...{ onDragover: () => { } },
        ...{ onDrop: (__VLS_ctx.handleDrop) },
        ...{ class: "upload-box" },
    });
    __VLS_asFunctionalElement(__VLS_intrinsicElements.input)({
        ...{ onChange: (__VLS_ctx.handleFileChange) },
        type: "file",
        id: "file-upload",
        accept: ".html,.xhtml",
        hidden: true,
    });
    __VLS_asFunctionalElement(__VLS_intrinsicElements.label, __VLS_intrinsicElements.label)({
        for: "file-upload",
    });
    if (!__VLS_ctx.selectedFile) {
        __VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({});
        __VLS_asFunctionalElement(__VLS_intrinsicElements.i, __VLS_intrinsicElements.i)({
            ...{ class: "bi bi-cloud-upload upload-icon" },
        });
        __VLS_asFunctionalElement(__VLS_intrinsicElements.p, __VLS_intrinsicElements.p)({});
    }
    else {
        __VLS_asFunctionalElement(__VLS_intrinsicElements.p, __VLS_intrinsicElements.p)({
            ...{ class: "selected-file" },
        });
        (__VLS_ctx.selectedFile.name);
    }
}
else {
    __VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({});
    for (const [file, index] of __VLS_getVForSourceType((__VLS_ctx.selectedFiles))) {
        __VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
            ...{ onDragover: () => { } },
            ...{ onDrop: ((e) => __VLS_ctx.handleDrop(e, index)) },
            key: (index),
            ...{ class: "upload-box" },
        });
        __VLS_asFunctionalElement(__VLS_intrinsicElements.input)({
            ...{ onChange: ((e) => __VLS_ctx.handleFileChange(e, index)) },
            type: "file",
            id: (`file-upload-${index}`),
            accept: ".html,.xhtml",
            hidden: true,
        });
        __VLS_asFunctionalElement(__VLS_intrinsicElements.label, __VLS_intrinsicElements.label)({
            for: (`file-upload-${index}`),
        });
        if (!file) {
            __VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({});
            __VLS_asFunctionalElement(__VLS_intrinsicElements.i, __VLS_intrinsicElements.i)({
                ...{ class: "bi bi-cloud-upload upload-icon" },
            });
            __VLS_asFunctionalElement(__VLS_intrinsicElements.p, __VLS_intrinsicElements.p)({});
            (index + 1);
        }
        else {
            __VLS_asFunctionalElement(__VLS_intrinsicElements.p, __VLS_intrinsicElements.p)({
                ...{ class: "selected-file" },
            });
            (file.name);
        }
        if (file) {
            __VLS_asFunctionalElement(__VLS_intrinsicElements.button, __VLS_intrinsicElements.button)({
                ...{ onClick: (...[$event]) => {
                        if (!!(__VLS_ctx.route.path !== '/merge-files'))
                            return;
                        if (!(file))
                            return;
                        __VLS_ctx.removeFile(index);
                    } },
                ...{ class: "remove-file" },
            });
        }
    }
}
__VLS_asFunctionalElement(__VLS_intrinsicElements.button, __VLS_intrinsicElements.button)({
    ...{ onClick: (__VLS_ctx.uploadFile) },
    disabled: (!__VLS_ctx.hasValidFiles || __VLS_ctx.isLoading),
});
if (!__VLS_ctx.isLoading) {
    __VLS_asFunctionalElement(__VLS_intrinsicElements.span, __VLS_intrinsicElements.span)({});
}
else {
    __VLS_asFunctionalElement(__VLS_intrinsicElements.span, __VLS_intrinsicElements.span)({
        ...{ class: "loader" },
    });
}
if (__VLS_ctx.isLoading) {
    __VLS_asFunctionalElement(__VLS_intrinsicElements.button, __VLS_intrinsicElements.button)({
        ...{ onClick: (__VLS_ctx.cancelUpload) },
        ...{ class: "annuler" },
    });
}
if (__VLS_ctx.fileError) {
    __VLS_asFunctionalElement(__VLS_intrinsicElements.p, __VLS_intrinsicElements.p)({
        ...{ class: "error-message" },
    });
    (__VLS_ctx.fileError);
}
/** @type {__VLS_StyleScopedClasses['container']} */ ;
/** @type {__VLS_StyleScopedClasses['description-box']} */ ;
/** @type {__VLS_StyleScopedClasses['upload-container']} */ ;
/** @type {__VLS_StyleScopedClasses['upload-content']} */ ;
/** @type {__VLS_StyleScopedClasses['upload-box']} */ ;
/** @type {__VLS_StyleScopedClasses['bi']} */ ;
/** @type {__VLS_StyleScopedClasses['bi-cloud-upload']} */ ;
/** @type {__VLS_StyleScopedClasses['upload-icon']} */ ;
/** @type {__VLS_StyleScopedClasses['selected-file']} */ ;
/** @type {__VLS_StyleScopedClasses['upload-box']} */ ;
/** @type {__VLS_StyleScopedClasses['bi']} */ ;
/** @type {__VLS_StyleScopedClasses['bi-cloud-upload']} */ ;
/** @type {__VLS_StyleScopedClasses['upload-icon']} */ ;
/** @type {__VLS_StyleScopedClasses['selected-file']} */ ;
/** @type {__VLS_StyleScopedClasses['remove-file']} */ ;
/** @type {__VLS_StyleScopedClasses['loader']} */ ;
/** @type {__VLS_StyleScopedClasses['annuler']} */ ;
/** @type {__VLS_StyleScopedClasses['error-message']} */ ;
var __VLS_dollars;
const __VLS_self = (await import('vue')).defineComponent({
    setup() {
        return {
            $props: __VLS_makeOptional(props),
            ...props,
            isLoading: isLoading,
            selectedFile: selectedFile,
            selectedFiles: selectedFiles,
            fileError: fileError,
            route: route,
            cancelUpload: cancelUpload,
            description: description,
            hasValidFiles: hasValidFiles,
            handleFileChange: handleFileChange,
            handleDrop: handleDrop,
            removeFile: removeFile,
            uploadFile: uploadFile,
        };
    },
});
export default (await import('vue')).defineComponent({
    setup() {
        return {
            $props: __VLS_makeOptional(props),
            ...props,
        };
    },
});
; /* PartiallyEnd: #4569/main.vue */
