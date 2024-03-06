
// .........SIDEBAE.........
const menuItem = document.querySelectorAll('.menu-item');
// remove active classList
const removeActive = () => {
    menuItem.forEach(item => {
        item.classList.remove('active');
    });
}


// CATEGORY


// MESSAGE


// STORIES


// THEME COSTOM

const themeMenu = document.querySelector('#themeMenu');
const themeBox = document.querySelector('.theme');

themeMenu.addEventListener('click', ()=>{
    themeBox.style.display="grid";
})

document.querySelector('.theme').addEventListener('click', ()=>{
    themeBox.style.display = "none";
});



// WINDOW EVENT
window.addEventListener('scroll', () =>{
    themeBox.style.display = 'none';

});

// FONT SIZE
const sizeThemes = document.querySelectorAll('[name="sizetheme"');
const colorThemes = document.querySelectorAll('[name="colortheme"');
const bgThemes = document.querySelectorAll('[name="bgtheme"');

// store theme
const storeSizeTheme = function( theme ) {
    localStorage.setItem('font-size', theme);
};
const storeColorTheme = function( theme ) {
    localStorage.setItem('color', theme);
};
const storeBgTheme = function( theme ) {
    localStorage.setItem('background', theme);
};

// apply theme
const retrieveTheme = function() {
    const activeSize = localStorage.getItem('font-size');
    const activeColor = localStorage.getItem('color');
    const activeBg = localStorage.getItem('background');

    sizeThemes.forEach((sizeOption) => {
        if (sizeOption.id === activeSize) {
            sizeOption.checked = true;
        };
    });

    colorThemes.forEach((colorOption) => {
        if (colorOption.id === activeColor) {
            colorOption.checked = true;
        };
    });

    bgThemes.forEach((bgOption) => {
        if (bgOption.id === activeBg) {
            bgOption.checked = true;
        };
    });

};

sizeThemes.forEach((sizeOption) => {
    sizeOption.addEventListener('click', () => {
        storeSizeTheme(sizeOption.id);
    });
});
colorThemes.forEach((colorOption) => {
    colorOption.addEventListener('click', () => {
        storeColorTheme(colorOption.id);
    });
});
bgThemes.forEach((bgOption) => {
    bgOption.addEventListener('click', () => {
        storeBgTheme(bgOption.id);
    });
});

function commentReplyToggle(parent_id) {
    const comment_reply_form = document.getElementById(parent_id);
	const comment_post_form = document.getElementById('comment_post_form');

    if (comment_reply_form.style.display === 'none') {
		console.log('click')
        comment_reply_form.style.display = 'block';
		comment_post_form.style.display = 'none';
    } else {
        comment_reply_form.style.display = 'none';
		comment_post_form.style.display = 'block';
    }
}


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function removeNotification(removeNotificationURL, redirectURL) {
	const csrftoken = getCookie('csrftoken');
	let xmlhttp = new XMLHttpRequest();

	xmlhttp.onreadystatechange = function() {
		if (xmlhttp.readyState == XMLHttpRequest.DONE) {
			if (xmlhttp.status == 200) {
				window.location.replace(redirectURL);
			} else {
				alert('There was an error');
			}
		}
	};

	xmlhttp.open("DELETE", removeNotificationURL, true);
	xmlhttp.setRequestHeader("X-CSRFToken", csrftoken);
	xmlhttp.send();
}

document.onload = retrieveTheme();

function formatTags() {
    const elements = document.getElementsByClassName("body");

    for (let i = 0; i < elements.length; i++) {
        let bodyText = elements[i].children[1].innerText;
        let words = bodyText.split(' ');
        for (let j = 0; j < words.length; j++) {
            if (words[j][0] === '#') {
                let replacedText = bodyText.replace(/\s#(.*?)(\s|$)/g, `<a href="/social/explore?query=${words[j].substring(1)}" class="tag-link">${words[j]}</a>`);
                elements[i].innerHTML = replacedText
            }
        }
    }
}

formatTags();