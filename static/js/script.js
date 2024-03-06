
// .........SIDEBAE.........
const menuItem = document.querySelectorAll('.menu-item');
// remove active classList
const removeActive = () => {
    menuItem.forEach(item => {
        item.classList.remove('active');
    });
}

menuItem.forEach(item => {
    item.addEventListener('click', () => {
        removeActive();
        item.classList.add('active');
        
        if (item.id != 'notifice'){
            document.querySelector('.notification').style.display = 'none';
        } else {
            document.querySelector('.notification').style.display = 'block';
            console.log(document.querySelector('.notification').style.display)
            document.querySelector('#notifice .count').style.display = "none";
        }

    });
});

// CATEGORY
const friends = document.querySelector('.friends');
const follow = document.querySelector('.follow');
const request = document.querySelector('.request-category');
const messageContainer = document.querySelector('.message-container-js');
const followContainer = document.querySelector('.follow-container-js');
const requestContainer = document.querySelectorAll('.friend-requests');

friends.addEventListener('click', () => {
    follow.classList.remove('active');
    friends.classList.add('active');
    followContainer.style.display = 'none';
    messageContainer.style.display = 'block';
});
follow.addEventListener('click', () => {
    friends.classList.remove('active');
    follow.classList.add('active');
    followContainer.style.display = 'block';
    messageContainer.style.display = 'none';
});
request.addEventListener('click', ()=>{
    requestContainer.forEach(element => {
        element.classList.add('box-sh-request');
        setTimeout(() => {
            element.classList.remove('box-sh-request');
        }, 3000);
    });
    
});


// MESSAGE
const message = document.querySelector('#message');
const messageBox = document.querySelector('#message-box');

message.addEventListener('click', ()=>{
    messageBox.classList.add('box-sh');
    message.querySelector('.count').style.display = 'none';
    
    setTimeout(() => {
        messageBox.classList.remove('box-sh');
    }, 3000);
});

// STORIES
const allStories = document.querySelectorAll(".stories-container .stories .story-image");
const allStoriesImg = document.querySelectorAll(".stories-container .stories .story .story-img");
const allStoriesAuthor = document.querySelectorAll(".stories-container .stories .story .author");
const allAuthorImg = document.querySelectorAll(".stories-container .story .profile-photos img");

const storiesFullView = document.querySelector(".stories-full-view");
const closeBtn = document.querySelector(".close-btn");

const storyImageFull = document.querySelector(".stories-full-view .story img");
const storyAuthorImgFull = document.querySelector(".stories-full-view .story .profile-photos img");

const nextBtn = document.querySelector(".stories-container .next-btn");
const previousBtn = document.querySelector(".stories-container .previous-btn");
const storiesContent = document.querySelector(".stories-container .content");
const nextBtnFull = document.querySelector(".stories-full-view .next-btn");
const previousBtnFull = document.querySelector(
    ".stories-full-view .previous-btn"
);

let currentActive = 0;
const createStories = () => {
    let id = 0
    allStories.forEach((s, i) => {
        s.setAttribute('id', id);
        s.addEventListener('click', () => {
            showFullView(s.id);
        });
        id++;
    });
};

createStories();

const showFullView = (index) => {
    currentActive = index;
    updateFullView(index);
    storiesFullView.classList.add('active');
};

closeBtn.addEventListener("click", () => {
    storiesFullView.classList.remove("active");
});

const updateFullView = (index) => {
    storyImageFull.src = allStoriesImg[index].src;
    storyAuthorImgFull.src = allAuthorImg[index].src;
};

nextBtn.addEventListener("click", () => {
    storiesContent.scrollLeft += 300;
});

previousBtn.addEventListener("click", () => {
    storiesContent.scrollLeft -= 300;
});

storiesContent.addEventListener("scroll", () => {
    if (storiesContent.scrollLeft <= 24) {
        previousBtn.classList.remove("active");
    } else {
        previousBtn.classList.add("active");
    }

    let maxScrollValue =
        storiesContent.scrollWidth - storiesContent.clientWidth - 24;

    if (storiesContent.scrollLeft >= maxScrollValue) {
        nextBtn.classList.remove("active");
    } else {
        nextBtn.classList.add("active");
    }
});

nextBtnFull.addEventListener("click", () => {
    if (currentActive >= allStories.length - 1) {
        return;
    }
    currentActive++;
    updateFullView(currentActive);
});

previousBtnFull.addEventListener("click", () => {
    if (currentActive <= 0) {
        return;
    }
    currentActive--;
    updateFullView(currentActive);
});


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
        console.log(bodyText);
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