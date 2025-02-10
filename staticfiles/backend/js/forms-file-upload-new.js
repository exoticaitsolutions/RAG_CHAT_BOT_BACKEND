/**
 * File Upload
 */

'use strict';

(function () {
  // previewTemplate: Updated Dropzone default previewTemplate
  // ! Don't change it unless you really know what you are doing
  const previewTemplate = `<div class="dz-preview dz-file-preview">
<div class="dz-details">
  <div class="dz-thumbnail">
    <img data-dz-thumbnail>
    <span class="dz-nopreview">No preview</span>
    <div class="dz-success-mark"></div>
    <div class="dz-error-mark"></div>
    <div class="dz-error-message"><span data-dz-errormessage></span></div>
    <div class="progress m-4">
      <div class="progress-bar progress-bar-primary m-2" role="progressbar" aria-valuemin="0" aria-valuemax="100" data-dz-uploadprogress></div>
    </div>
  </div>
  <div class="dz-filename" data-dz-name></div>
  <div class="dz-size" data-dz-size></div>
</div>
</div>`;

  // ? Start your code from here

  // Basic Dropzone
  // --------------------------------------------------------------------
  const dropzoneBasic = document.querySelector('#dropzone-basic');
  if (dropzoneBasic) {
    const myDropzone = new Dropzone(dropzoneBasic, {
      previewTemplate: previewTemplate,
      parallelUploads: 5,
      maxFilesize: 50,
      addRemoveLinks: true,
      maxFiles: 10
    });
  }

  // Multiple Dropzone
  // --------------------------------------------------------------------
  // const dropzoneMulti = document.querySelector('#dropzone-multi');
  // if (dropzoneMulti) {
  //   const myDropzoneMulti = new Dropzone(dropzoneMulti, {
  //     previewTemplate: previewTemplate,
  //     uploadMultiple: true,
  //     parallelUploads: 20,
  //     maxFilesize: 50,
  //     addRemoveLinks: true,
  //     autoProcessQueue: false, // Disable auto upload
  //     acceptedFiles: ".pdf, .csv, .docx, .txt"
  //   });
  // }
    // const dropzoneMulti = document.querySelector('#dropzone-multi');
    // if (dropzoneMulti) {
    //     const myDropzoneMulti = new Dropzone(dropzoneMulti, {
    //         previewTemplate: previewTemplate,
    //         uploadMultiple: true,
    //         parallelUploads: 25,
    //         maxFilesize: 100,
    //         addRemoveLinks: true,
    //         autoProcessQueue: false, // Disable auto upload
    //         acceptedFiles: ".pdf, .csv, .docx, .txt, .ppt"
    //     });

    //     // Add a success event listener to refresh the page after all files are uploaded
    //     myDropzoneMulti.on("success", function (file, response) {
    //         if (myDropzoneMulti.getQueuedFiles().length === 0 && myDropzoneMulti.getUploadingFiles().length === 0) {
    //             location.reload(); // Refresh the page
    //         }
    //     });

    //     // Add an error event listener to display an error message if any files fail to upload
    //     myDropzoneMulti.on("error", function (file, errorMessage, xhr) {
    //         Swal.fire('Error', 'An error occurred while uploading the files.', 'error');
    //     });

    //     const submitUploadButton = document.querySelector('#submit-upload');
    //     if (submitUploadButton) {
    //         submitUploadButton.addEventListener('click', function () {
    //             if (myDropzoneMulti.getQueuedFiles().length > 0) {
    //                 Swal.fire({
    //                     title: 'Confirm Upload',
    //                     text: 'Are you sure you want to upload the selected files?',
    //                     icon: 'question',
    //                     showCancelButton: true,
    //                     confirmButtonText: 'Upload',
    //                     cancelButtonText: 'Cancel',
    //                     customClass: {
    //                       cancelButton: 'swal2-cancel btn btn-label-danger',
    //                       confirmButton: 'swal2-confirm btn btn-primary px-5',
    //                       denyButton: 'd-none',
    //                   }
    //                 }).then((result) => {
    //                     if (result.isConfirmed) {
    //                         myDropzoneMulti.processQueue(function () {
    //                             dropzoneMulti.submit(); // Submit the form after all files are uploaded
    //                             Swal.fire(   'Successfully File Uploaded.','success')
    //                         });
    //                     }
    //                 });
    //             } else {
    //                 Swal.fire({
    //                   title: 'No Files',
    //                   text: 'Please add to files upload.',
    //                   icon: 'warning',
    //                   showCancelButton: true,
    //                   cancelButtonText: 'Back',
    //                   customClass: {
    //                     cancelButton: 'swal2-cancel btn btn-label-info',
    //                     confirmButton: 'd-none',
    //                     denyButton: 'd-none',
    //                 }
    //               });
    //             }
    //         });
    //     }
    // }

const dropzoneMulti = document.querySelector('#dropzone-multi');
if (dropzoneMulti) {
    const myDropzoneMulti = new Dropzone(dropzoneMulti, {
        previewTemplate: previewTemplate,
        uploadMultiple: true,
        parallelUploads: 25,
        maxFilesize: 100,
        addRemoveLinks: true,
        autoProcessQueue: false, // Disable auto upload
        acceptedFiles: ".pdf, .csv, .docx, .txt, .ppt, .pptx"
    });

    // Add a success event listener to refresh the page after all files are uploaded
    myDropzoneMulti.on("success", function (file, response) {
        console.log("_____________________________")
        var show_alert = document.getElementById("show_alert");
        show_alert.classList.add("d-none");
        if (myDropzoneMulti.getQueuedFiles().length === 0 && myDropzoneMulti.getUploadingFiles().length === 0) {
            location.reload(); // Refresh the page
        }
    });

    // Add an error event listener to display an error message if any files fail to upload
    myDropzoneMulti.on("error", function (file, errorMessage, xhr) {
        Swal.fire('Error', 'An error occurred while uploading the files.', 'error');
    });

    const submitUploadButton = document.querySelector('#submit-upload');
    if (submitUploadButton) {
        submitUploadButton.addEventListener('click', function () {
            const files = myDropzoneMulti.getQueuedFiles();
            const oversizedFiles = files.filter(file => file.size > 100 * 1024 * 1024); // Check for files larger than 100 MB (100 * 1024 * 1024 bytes)

            var show_alert = document.getElementById("show_alert");
            show_alert.classList.add("d-none");

            if (oversizedFiles.length > 0) {
                show_alert.classList.remove("d-none")
                show_alert.innerHTML = 'File is Over Sized, Please select other file.'
            } else if (files.length > 0) {
                myDropzoneMulti.processQueue(function () {
                    dropzoneMulti.submit(); // Submit the form after all files are uploaded
                    Swal.fire('Successfully File Uploaded.', 'success');

                });
            } else {
                show_alert.classList.remove("d-none")
                show_alert.innerHTML = 'Please select a File.'
            }
        });
    }
}


})();
