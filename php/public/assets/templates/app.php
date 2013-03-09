<!DOCTYPE html>
<html>
	<head>
		<link rel='stylesheet' type='text/css' href='./assets/css/bootstrap.css' />
		<link rel='stylesheet' type='text/css' href='./assets/css/lan.css' />
	</head>
	<body>
		
		<div id='wrapper' class='row-fluid'>
		    <div class='span4'>
			    <div class='pane'>
			        <div class='pane-content'>
				        <h2>Queue</h2>
				        <table id='queue'>
					        <tbody>
					        </tbody>
				        </table>
				    </div>
				</div>
			</div>
		    <div class='span4'>
			    <div class='pane' id='matches'>
			        <div class='pane-content'>
	    			    <h2>Matches Being Set Up</h2>
				</div>
			</div>
		    </div>
		    <div class='span4'>
			    <div class='pane' id='activeMatches'>
			        <div class='pane-content'>
    				    <h2>Active Matches</h2>
				</div>
			</div>
		    </div>
		</div>
		
		<div id='header'>
			<!--<button id='play'>Play</button>
			<button id='callGroup'>Call Group</button>-->
		</div>
		
		<script src="./assets/js/mustache.js" type="text/javascript"></script>
		<script src="./assets/js/utils.js" type="text/javascript"></script>
		<script src="./assets/js/engine.js" type="text/javascript"></script>
		<script id="active-match" type="text/x-mustache-template"></script>
		<script id="match" type="text/x-mustache-template"></script>
		<script type='text/javascript'></script>
	
	</body>
</html>
